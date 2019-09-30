# The Environment Contract
## Why?
In many applications, especially [twelve-factor](https://12factor.net/) ones, configuration information is provided to the application via the environment.

### Safety
Missing or incorrect environment information can result in crashes, undefined behavior, and data loss. By protecting configuration with a schema, we can fail fast and safely abort a deploy.

### Clarity
A developer configuring a new environment by copying an existing one may not be aware of their range of options, leading them to guess at the configuration. Making an implicit contract explicit streamlines onboarding and prevents regressions.

A good contract will also include documentation, further improving clarity. Documentation in the schema is less likely to fall out of date than if it lives in a readme or external documentation.

### Simplicity
In applications I've used that lack an environment contract, environment variables are validated repeatedly throughout the codebase. Adding a contract consolidates the validation logic and applies it once on startup, improving reuse and reducing surface area for bugs.

## How?
Since the environment is a string-to-string mapping, it is easily modeled as a dictionary and validated by a [JSON schema](https://json-schema.org). This repo includes [an example](environment.schema.json).

### Requirements
JSON Schema allows specifying which fields are required:
```
  "required": [
    "APP_NAME",
    "DEPENDENCY_URL",
    "DEPENDENCY_VERSION"
  ],
```

I recommend allowing unspecified properties via the `additionalProperties` flag. For most applications, validating every system-defined environment variable seems like maintenance-inducing overkill.

### Descriptions
JSON Schema includes a `description` element, which should be used to describe the purpose of the variable:
```
    "DEPENDENCY_VERSION": {
      "type": "string",
      "description": "In some environments, this application runs against DEPENDENCY VERSION X, while in others it runs against VERSION Y.",
    },
```

### Typing
Since everything in the environment is a string, the schema must validate all properties as a string:
```
    "TIMEOUT": {
      "type": "string",
      "description": "Timeout duration for calls to DEPENDENCY Z",
    }
```

To validate properties further, JSON Schema supports regex:
```
    "TIMEOUT": {
      ...,
      "pattern": "^\\d{1,5}$"
    }
```
In this example, `TIMEOUT` is required to be a 1-5 digit number.

## Demo
This application provides [Node](node/example.js) and [Python](python/example.py) examples. If you would like to contribute additional examples, I encourage you to contact me and open a PR.

The examples below use the node script, but should function similarly in all examples.

### Success
```
APP_NAME=ex DEPENDENCY_URL=http://subdomain.domain.com/api/v4 DEPENDENCY_VERSION=3.2.1 TIMEOUT=5000 node example.js
```

### Require App Name
```
DEPENDENCY_URL=http://subdomain.domain.com/api/v4 DEPENDENCY_VERSION=3.2.1 TIMEOUT=5000 node example.js
{ [Error: validation failed]
  message: 'validation failed',
  errors:
   [ { keyword: 'required',
       dataPath: '',
       schemaPath: '#/required',
       params: [Object],
       message: 'should have required property \'APP_NAME\'' } ],
  validation: true,
  ajv: true }
```
### URL Format
```
APP_NAME=ex DEPENDENCY_URL=htp://subdomain.domain.com/api/v4 DEPENDENCY_VERSION=3.2.1 TIMEOUT=60000 node example.js
{ [Error: validation failed]
  message: 'validation failed',
  errors:
   [ { keyword: 'pattern',
       dataPath: '.DEPENDENCY_URL',
       schemaPath: '#/properties/DEPENDENCY_URL/pattern',
       params: [Object],
       message: 'should match pattern "^((http[s]?|ftp):\\/)?\\/?([^:\\/\\s]+)((\\/\\w+)*/)([\\w\\-\\.]+[^#?\\s]+)(.*)?(#[\\w\\-]+)?$"' } ],
  validation: true,
  ajv: true }
```

### Version Format
```
APP_NAME=ex DEPENDENCY_URL=http://subdomain.domain.com/api/v4 DEPENDENCY_VERSION=3.2 TIMEOUT=60000 node example.js
{ [Error: validation failed]
  message: 'validation failed',
  errors:
   [ { keyword: 'pattern',
       dataPath: '.DEPENDENCY_VERSION',
       schemaPath: '#/properties/DEPENDENCY_VERSION/pattern',
       params: [Object],
       message: 'should match pattern "^(\\d+)\\.(\\d+)\\.(\\d+)$"' } ],
  validation: true,
  ajv: true }
```

### Timeout Format
Require `TIMEOUT` to be a 1-5 digit string.
```
APP_NAME=ex DEPENDENCY_URL=http://subdomain.domain.com/api/v4 DEPENDENCY_VERSION=3.2.1 TIMEOUT=none node example.js
{ [Error: validation failed]
  message: 'validation failed',
  errors:
   [ { keyword: 'pattern',
       dataPath: '.TIMEOUT',
       schemaPath: '#/properties/TIMEOUT/pattern',
       params: [Object],
       message: 'should match pattern "^\\d{1,5}$"' } ],
  validation: true,
  ajv: true }
```
```
APP_NAME=ex DEPENDENCY_URL=http://subdomain.domain.com/api/v4 DEPENDENCY_VERSION=3.2.1 TIMEOUT=600000 node example.js
{ [Error: validation failed]
  message: 'validation failed',
  errors:
   [ { keyword: 'pattern',
       dataPath: '.TIMEOUT',
       schemaPath: '#/properties/TIMEOUT/pattern',
       params: [Object],
       message: 'should match pattern "^\\d{1,5}$"' } ],
  validation: true,
  ajv: true }
```
