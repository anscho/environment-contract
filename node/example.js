const Ajv = require('ajv')
const schema = require('../environment.schema')

const ajv = new Ajv()
const schema_validator = ajv.compile({
  ...schema,
  '$async': true
})

schema_validator(process.env).catch(console.error)
