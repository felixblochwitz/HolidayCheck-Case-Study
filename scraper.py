import requests as req
import pandas as pd
import json


# building api request string
api_key = "91f67b2a-520b-4f9f-a4ca-edcb0d610454"
# NOTE: api documentation: https://open-platform.theguardian.com/documentation/


# how to pretty print json
# result = req.get(test_str).content
# parsed = json.loads(result)
# print(json.dumps(parsed, indent=4, sort_keys=True))


def api_wrapper(query, start_date, api_key):
    api_str = f'https://content.guardianapis.com/search?q="{query}"&from-date={start_date}&order-by=oldest&api-key={api_key}&type=article&query-fields=headline'

    response = req.get(api_str).content
    response_json = json.loads(response)
    return response_json


my_json = api_wrapper("trudeau", "2018-01-01", api_key)

print(my_json['response'])

# print(req.get("http://content.guardianapis.com/tags?q=Trudeau&api-key=91f67b2a-520b-4f9f-a4ca-edcb0d610454").content)