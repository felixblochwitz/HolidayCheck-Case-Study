import requests as req
import json


# building api request string
start_date = "" #in format yyyy-mm-dd
api_key = "91f67b2a-520b-4f9f-a4ca-edcb0d610454"
query = 
#NOTE: api documentation: https://open-platform.theguardian.com/documentation/
api_str = f'https://content.guardianapis.com/search?q="{query}"&from-date={start_date}&api-key={api_key}'




# how to pretty print json
result = req.get(test_str).content
parsed = json.loads(result)
print(json.dumps(parsed, indent=4, sort_keys=True))



