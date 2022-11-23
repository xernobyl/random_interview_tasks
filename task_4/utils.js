/*
utils.js
*/

import settings from './settings.json' assert { type: 'json' }

/*
function getSettings () {
  let result = null

  fs.readFile('./settings.json', 'utf8', (err, data) => {
    if (err) {
      console.log(`Error reading file from disk: ${err}`)
    } else {
      console.log('Read file.')

      result = data
    }
  })

  return result
}
*/

const debugLog = settings.debug ? console.log : () => {}

export { debugLog }
