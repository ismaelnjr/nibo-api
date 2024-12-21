import requests

url = "https://api.nibo.com.br/empresas/v1/customers/FormatType=json"

import requests

url = "https://api.nibo.com.br/empresas/v1/schedules/credit"

payload = {
    "categories": [
        {
            "categoryId": "03708e32-f12f-4f57-9893-11d15864c7ce",
            "value": "100",
            "description": "TESTE"
        }
    ],
    "stakeholderId": "48dd1c64-40bf-4590-bd94-bf1318db74e1",
    "scheduleDate": "11/11/2024",
    "dueDate": "11/11/2024",
    "description": "AAAAAA",
    "reference": "BBBBBB"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "apitoken": "4B47856F452D484ABB5912CE4EB5D02E"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
