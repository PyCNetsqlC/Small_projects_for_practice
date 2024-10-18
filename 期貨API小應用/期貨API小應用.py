import requests
import json,csv
import copy
 



# API URL
url = "https://openapi.taifex.com.tw/v1/MarketDataOfMajorInstitutionalTradersDetailsOfFuturesContractsBytheDate"

# 發送 GET 請求
response = requests.get(url)

# 確認請求成功
if response.status_code == 200:
    # 將回應解析為 JSON
    data = response.json()

    # 篩選條件: ContractCode 為 "臺股期貨" 且 Item 為 "外資及陸資"
    filtered_data = [item for item in data if item['ContractCode'] == "臺股期貨" and item['Item'] == "外資及陸資"]

else:
    print(f"Error: Unable to fetch data (status code: {response.status_code})")


#篩選目標數據
extracted_data = list(map(lambda row: {'Date': row['Date'], 'ContractCode': row['ContractCode'], 'TradingVolume(Long)': row['TradingVolume(Long)'], 'TradingVolume(Short)': row['TradingVolume(Short)']}, filtered_data))

#提取表頭
a = extracted_data[0].keys()
w = []
for i in a:
    w.append(i)

#增添表頭
header_extracted_data = copy.deepcopy(extracted_data)

#修改表頭
for i in range(len(header_extracted_data[0])):
    n = w[i]
    if i==2:
        n = "交易量(多頭)"
    elif i==3:
        n = "交易量(空頭)"
    header_extracted_data[0][w[i]] = n



#數據整合
header_extracted_data.append(extracted_data[0])



with open("you_want.csv","w",encoding="utf-8-sig",newline='') as d:

    #csv 宣告
    writer = csv.writer(d)

    #容器s"List s"
    s = []
    #容器x"List x"
    x = []

    #整理extracted_data_header總數據，提取目標數值並填入容器s"List s"
    for i in range(len(header_extracted_data)):
        for j in w:
            rtt = f"{header_extracted_data[i][j]}"
            s.append(rtt)

    #整理容器s數據，提取目標數值並填入容器x"List x"
    for i in range(4,len(s)+4):
        if i%4==0:
            x.append(s[i-4:i])

    #提取容器x目標數值並填入you_want.csv
    for i in x:
        writer.writerow(i)
    