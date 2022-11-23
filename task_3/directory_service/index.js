/*
Directory service for ~REDACTED~

~REDACTED~

Fully asynchronous, and does not use GraphQL. Sorry.
*/


import settings from './settings.json' assert { type: 'json' }
import express from 'express'
import path from 'path'
import compression from 'compression'
import { opendir, lstat, access, constants } from 'node:fs/promises'
import { accessSync, statSync } from 'fs'

// initial sanity checks: root can be accessed
try {
  accessSync(settings.root_directory, constants.R_OK)
} catch {
  console.log(`Impossible to access "${settings.root_directory}".`)
  process.exit(1)
}

// initial sanity checks: root is directory
const stats = statSync(settings.root_directory)
if (!stats.isDirectory()) {
  console.log(`"${settings.root_directory}" is not a directory.`)
  process.exit(1)
}

// initialize Express
const app = express()
app.use(compression())
app.use(express.json())

// set allowed CORS domains
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', settings.cors_allowed_domains)
  next()
})

// get files
app.get('/files/*', async (req, res) => {
  const file_list = []

  // prefix the base path to the requested path
  const base_path = path.join(settings.root_directory, req.params[0])

  // check if we can access the requested path
  try {
    await access(base_path, constants.R_OK);
  } catch {
    const error_message = `Cannot access "${base_path}".`
    res.send({ error: error_message })
    return
  }

  // check if requested path is a directory
  const stats = await lstat(base_path)
  if (!stats.isDirectory()) {
    const error_message = `"${base_path}" is not a directory.`
    res.send({ error: error_message })
    return
  }

  try {
    const dir = await opendir(base_path)  // open directory
    for await (const dirent of dir) {     // go over each file (in the unix sense) in the directory
      const file_path = path.join(base_path, dirent.name) // get full file path
      const stats = await lstat(file_path)                // get file stats

      // set a few example file properties...
      const file_data = {
        file_name: dirent.name,
      }

      if (stats.isBlockDevice()) {
        file_data.file_type = 'block device'
      } else if (stats.isCharacterDevice()) {
        file_data.file_type = 'character device'
      } else if (stats.isDirectory()) {
        file_data.file_type = 'directory'
      } else if (stats.isFIFO()) {
        file_data.file_type = 'fifo'
      } else if (stats.isFile()) {
        file_data.file_size = stats.size
        file_data.file_type = 'file'
      } else {
        file_data.file_type = 'unknown'
      }

      file_list.push(file_data)
    }

    // return list of files
    res.send({
      files: file_list
    })
  } catch (err) {
    console.error(`Error: ${err}`)
  }
})

// initialize server
const server = app.listen(settings.port, () => {
  const address = server.address()
  const host = address.address
  const port = address.port
  console.log(`Directory service working at http://${host}:${port}`)
})
