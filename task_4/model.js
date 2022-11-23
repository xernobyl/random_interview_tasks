/*
crud model - Create, read, update and delete
*/

import { debugLog } from './utils.js'
import { FieldType } from './field.js'

export class Model {
  static register (app) {
    if (this.fields === undefined) {
      this.fields = {}
    } else {
      for (const field in this.fields) {
        const fieldType = this.fields[field]
        if (!(fieldType in Object.values(FieldType))) {
          throw new Error(`${fieldType} is an invalid FieldType`)
        }
      }
    }

    const className = this.prototype.constructor.name.toLowerCase()
    const baseUrl = `/${className}`
    const idUrl = baseUrl + '/:id'

    debugLog(`registering "${className}":`)

    // create
    debugLog(`\tregistering POST ${baseUrl}`)
    app.post(baseUrl, (req, res) => {
      if (typeof req.body !== 'object') {
        res.send(500)
        return
      }

      try {
        const newInstance = new this(req.body)
        res.json(newInstance.serialize())
      } catch (e) {
        debugLog(e)
        res.send(500)
      }
    })

    // read
    debugLog(`\tregistering GET ${baseUrl}`)
    app.get(baseUrl, (req, res) => {
      res.send(`here's all ${className}s`)
    })

    debugLog(`\tregistering GET ${idUrl}`)
    app.get(idUrl, (req, res) => {
      const id = req.params.id
      res.send(`here's ${className} (${id})`)
    })

    // update
    debugLog(`\tregistering PUT ${baseUrl}`)
    app.put(baseUrl, (req, res) => {
      res.send(`here's all ${className}s`)
    })

    debugLog(`\tregistering PUT ${idUrl}`)
    app.put(idUrl, (req, res) => {
      const id = req.params.id
      res.send(`here's ${className} (${id})`)
    })

    // delete
    debugLog(`\tregistering DELETE ${idUrl}`)
    app.delete(idUrl, (req, res) => {
      const id = req.params.id
      res.send(`deleting ${className} ${id}`)
    })

    // TODO: batch delete
  }

  constructor (data) {
    // a simple deserializer

    debugLog('Model::constructor')
    for (const fieldName in this.constructor.fields) {
      const fieldType = this.constructor.fields[fieldName]

      switch (fieldType) {
        case FieldType.Number:
          try {
            this[fieldName] = Number(data[fieldName])
          } catch (e) {
            throw new Error(`${fieldName}: ${data[fieldName]} is an invalid Number`)
          }
          break

        case FieldType.String:
          try {
            this[fieldName] = String(data[fieldName])
          } catch (e) {
            throw new Error(`${fieldName}: ${data[fieldName]} is an invalid String`)
          }
          break

        case FieldType.Bool:
          try {
            this[fieldName] = Boolean(data[fieldName])
          } catch (e) {
            throw new Error(`${fieldName}: ${data[fieldName]} is an invalid Bool`)
          }
          break

        default:
          throw new Error(`${fieldType} is an invalid FieldType`)
      }
    }
  }

  serialize () {
    const outputDict = {}

    for (const fieldName in this.constructor.fields) {
      const fieldType = this.constructor.fields[fieldName]

      switch (fieldType) {
        case FieldType.Number:
        case FieldType.String:
        case FieldType.Bool:
        default:
          outputDict[fieldName] = this[fieldName]
      }
    }

    return outputDict
  }
}
