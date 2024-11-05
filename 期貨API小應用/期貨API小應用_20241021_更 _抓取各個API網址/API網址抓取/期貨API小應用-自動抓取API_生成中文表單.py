import requests
import json


url="https://openapi.taifex.com.tw/swagger.json"


# 發送 GET 請求
response = requests.get(url)

# 確認請求成功
if response.status_code == 200:
    # 將回應解析為 JSON
    data_API = response.json()

    #All data Key
    data_API_Key = list(data_API.keys())
    
    #API網址
    data_API_str = ["https://openapi.taifex.com.tw/v1"+i for i in list(data_API["paths"].keys())]
    
    #API網址chinese title
    data_ch_show_str = [(data_API["paths"][list(data_API["paths"].keys())[i]]["get"]['summary']) for i in range(len(data_API_str))]

    data_fromload = dict(zip([(data_API["paths"][list(data_API["paths"].keys())[i]]["get"]['summary']) for i in range(len(list(data_API["paths"].keys())))],["https://openapi.taifex.com.tw/v1"+i for i in list(data_API["paths"].keys())]))
    


    #功能測試碼
    url = '三大法人-區分各期貨契約-依日期'

    response_New = requests.get(data_fromload[url])

    if response.status_code == 200:
        data_New = response_New.json()
        



    with open("rightline.txt","w",encoding="utf-8-sig") as file:
        for i in data_fromload:
            file.write(f"{i}: {data_fromload[i]}\n\n")


