
#%%
api_key="xyz" 
port="8108"
schema_name = "targetname"


#%%
import typesense


def _alias_create_api(ip="localhost", port=port, key=api_key):
    return typesense.Client({
    'api_key': key,
    'nodes': [{
        'host': ip,
        'port': port,
        'protocol': 'http'
    }],
    'connection_timeout_seconds': 2
    })
    
def _query_by_alias(client, alias : str):
    search_parameters = {
    'q'         : alias,
    'query_by'  : 'alias',
    # 'filter_by' : 'publication_year:<1998',
    # 'sort_by'   : 'ratings_count:desc'
    }
    ret = client.collections[schema_name].documents.search(search_parameters)
    # print(ret["hits"])
    res = []
    for item in ret["hits"]:
        # print(item)
        doc = {k :item["document"][k] for k in ["alias", "name", "location"]}
        doc["alias"] = item["highlight"]["alias"]["snippet"]
        res.append(doc)
    return res


client = _alias_create_api("localhost", port, api_key)

def query_by_alias(alias:str):
    return _query_by_alias(client, alias)
#%%

if __name__ == "__main__" :
    print(query_by_alias("志航"))
# %%
