import requests
import json

url = "https://api.nibo.com.br/empresas/v1/customers"

headers = {
    "accept": "application/json",
    "apitoken": "4B47856F452D484ABB5912CE4EB5D02E" 
}

params = {
    "$filter": "document/number eq '11497110000127'"
}

try:

    response = requests.get(url, params=params, headers=headers)
    y = json.loads(response.text)
    #print(y)
    for item in y["items"]: 
        print(f"id: {item["id"]}")
        print(f"name: {item["name"]}")
        print(f"document/number: {item["document"]["number"]}")
        print(f"document/type: {item["document"]["type"]}")


except Exception as ex:
    print(f"Erro ao conectar no nibo: {ex}")
