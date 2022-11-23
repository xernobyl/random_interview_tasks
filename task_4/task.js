import { Model } from './model.js'
import { FieldType } from './field.js'
import { debugLog } from './utils.js'

export class Task extends Model {
  static fields = {
    text: FieldType.String
  }

  constructor (data) {
    super(data)
    debugLog('Task::constructor')
  }
}
