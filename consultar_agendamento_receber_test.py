import requests
import json

url = "https://api.nibo.com.br/empresas/v1/schedules/credit/opened"

headers = {
    "accept": "application/json",
    "apitoken": "4B47856F452D484ABB5912CE4EB5D02E"  
}

params = {
    "$filter": "stakeholder/cpfCnpj eq '11497110000127'"
}


try:

    response = requests.get(url, params=params, headers=headers)
    y = json.loads(response.text)
    i = 1
    for item in y["items"]: 
        for categoryList in item["categories"]:
            print(f"categoryName ({i}): {categoryList["categoryName"]}, value: {categoryList["value"]}")
            i+=1

    print(f"description: {item["description"]}")    
    print(f"reference: {item["reference"]}")
    print(f"openValue: {item["openValue"]}")
    print(f"paidValue: {item["paidValue"]}")
    print(f"dueDate: {item["dueDate"]}")
    print(f"accrualDate: {item["accrualDate"]}")
    print(f"scheduleDate: {item["scheduleDate"]}")

except Exception as ex:
    print(f"Erro ao conectar no nibo: {ex}")
