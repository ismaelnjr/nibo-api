import requests
import json

url = "https://api.nibo.com.br/empresas/v1/schedules/categories"

headers = {
    "accept": "application/json",
    "apitoken": "4B47856F452D484ABB5912CE4EB5D02E" 
}
""""
params = {
    "$filter": "name eq '3.01.01 - Vendas de produção'"
}
"""
params = {
    "$filter": "type eq 'in'"
}

try:

    response = requests.get(url, params=params, headers=headers)
    y = json.loads(response.text)
    print(y)
    i = 0
    for item in y["items"]: 
        print(f"({i})")
        print(f"id: {item["id"]}")
        print(f"name: {item["name"]}")
        i+=1

except Exception as ex:
    print(f"Erro ao conectar no nibo: {ex}")
