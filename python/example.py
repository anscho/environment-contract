import json
import os
from jsonschema import validate

with open('../environment.schema.json') as schema_file:
    schema_string = schema_file.read()

schema = json.loads(schema_string)

# Copying `os.environ` appears to turn it
# from whatever it is into a proper dict
env = os.environ.copy()
validate(instance=env, schema=schema)
