import requests

url = "https://api.nibo.com.br/empresas/v1/customers/FormatType=json"

payload = {
    "document": {
        "type": "cnpj",
        "number": "11497110000127"
    },
    "name": "NASCIMENTO CONTABILIDADE"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "apitoken": "4B47856F452D484ABB5912CE4EB5D02E"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)