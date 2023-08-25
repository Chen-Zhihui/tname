import typesense

# config
schema_name = "targetname"
data_file = "./alias.jsonl"

# init client
client = typesense.Client({
  'api_key': 'xyz',
  'nodes': [{
    'host': 'localhost',
    'port': '8108',
    'protocol': 'http'
  }],
  'connection_timeout_seconds': 2
})

# create schema
targetname_schema = {
  'name': f'{schema_name}',
  'fields': [
    {'name': 'country', 'type': 'string', 'facet': True },
    {'name': 'language', 'type': 'string', 'facet': True },
    {'name': 'target_type', 'type': 'string', 'facet': True },
    {'name': 'alias_id', 'type': 'string' },
    {'name': 'target_id', 'type': 'string' },
    {'name': 'alias', 'type': 'string', "sort" : True },
    {'name': 'name', 'type': 'string', "sort" : True  },
    {'name': 'location', 'type': 'geopoint'},
  ],
  'default_sorting_field': 'alias'
}

create_response = client.collections.create(targetname_schema)

# import json lines
with open(data_file) as jsonl_file:
    client.collections[f'{schema_name}'].documents.import_(jsonl_file.read().encode("utf-8"))

# retrieve information for collection
client.collections[f'{schema_name}'].retrieve()

# drop a collection
client.collections[f'{schema_name}'].delete()