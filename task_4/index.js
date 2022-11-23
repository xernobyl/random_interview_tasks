import settings from './settings.json' assert { type: 'json' }
import { Task } from './task.js'
import express from 'express'

const app = express()
app.use(express.json())

app.get('/', (req, res) => {
  res.send('TODO maybe inserting something useful here?')
})

const server = app.listen(settings.port, () => {
  const address = server.address()
  const host = address.address
  const port = address.port
  console.log(`Tasks working at http://${host}:${port}`)
})

Task.register(app)
