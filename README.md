# The Environment Contract

## Running example.js
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
