# The Environment Contract
## Why?
In many applications, especially those ascribing to [The Twelve-Factor App](https://12factor.net/), configuration information is provided to the application via the environment.

### Safety
If environment information is missing or incorrect, it could result in crashes, undefined behavior, or data loss. It's preferable to fail fast and abort a deploy. For this reason, the environment should be protected by a schema.

### Clarity
Like any contract, making the implicit explicit has benefits to clarity. A developer configuring a new environment by copying an existing one may not be aware of their range of options, leading them to guess at the configuration.

A good contract will also include documentation, further improving clarity. When that documentation lives in the schema, it is less likely to fall out of date than if it lives in a readme or external documentation.

### Simplicity
In applications I've used that lack an environment contract, environment variables are re-validated throughout the codebase. Adding this contract consolidates the validation logic and applies it once on startup, improving reuse and reducing surface area for bugs.

## How?
Since the environment is a string-to-string mapping, it is easily modeled as a dictionary and validated by [a JSON schema](https://json-schema.org). This repo includes [an example](environment.schema.json).

### Requirements
JSON Schema allows specification of which fields are required:
```
  "required": [
    "APP_NAME",
    "DEPENDENCY_URL",
    "DEPENDENCY_VERSION"
  ],
```

Given that the developer does not fully control the system environment, it seems cost-ineffective to specify every system-defined environment variable. In that light, I recommend allowing non-specified properties via the `additionalProperties` flag.

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
