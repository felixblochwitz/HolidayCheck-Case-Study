import requests as req
import json


# building api request string
api_key = "91f67b2a-520b-4f9f-a4ca-edcb0d610454"
# NOTE: api documentation: https://open-platform.theguardian.com/documentation/


# how to pretty print json
# result = req.get(test_str).content
# parsed = json.loads(result)
# print(json.dumps(parsed, indent=4, sort_keys=True))


def api_wrapper(query, start_date, api_key):
    api_str = f'https://content.guardianapis.com/search?q="{query}"&from-date={start_date}&api-key={api_key}'

    result_json = req.get(api_str).content
    return result_json


my_json = api_wrapper("Trudeau", "2022-02-22", api_key)

print(my_json)
