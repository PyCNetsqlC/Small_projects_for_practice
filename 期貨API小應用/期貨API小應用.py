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
    #data的原始總資料
    original_data_all = [item for item in data] #or copy.deepcopy(data)
    # data's key
    data_key = list(data[0].keys())
    #Chinese Title
    data_ch_title = ['日期', '合約代碼', '項目', '多單交易量', '多單交易值（千元）', '空單交易量', '空單交易值（千元）', '淨交易量', '淨交易值（千元）', '多單未平倉量', '多單未平倉合約價值（千元）', '空單未平倉量', '空單未平倉合約價值（千元）', '未平倉淨額', '未平倉合約淨值（千元）']
    #Chinese Title暫容器
    data_sort = dict()
    for i in range(len(data_key)):
        data_sort[data_key[i]] = data_ch_title[i]
    #在總資料中添加中文標籤
    data = data+copy.deepcopy([data_sort])
    #釋放暫容器空間
    del(data_sort)  
    #
    #篩選條件(GUI選單處): ContractCode 為 "臺股期貨" 且 Item 為 "外資及陸資"
    #filtered_data = [item for item in data if item['ContractCode'] == "臺股期貨" and item['Item'] == "外資及陸資"]
    #filtered_data = set([item for item in data if item['ContractCode'] == "臺股期貨"])# and item['Item'] == "外資及陸資"]
    
else:
    print(f"Error: Unable to fetch data (status code: {response.status_code})")


#篩選目標數據
#extracted_data_1 = list(map(lambda row: filtered_data[0], filtered_data))

'''seen = set() #check title is sole
extracted_data_1 = [] #Correspond data about title
    
# GUIform_Alldata & GUIform_Alldata_Corresponddata
for item in data:
    key = (item['ContractCode'], item['Item'])
    if key[0]!='合約代碼' and key[1]!='項目':
        extracted_data_1.append(item)
        seen.add(key)

#(GUI_form_A & GUI_form_B)'s Options

listseen_GUIform_A = list()#GUI_form_A
listseen_GUIform_B = list()#GUI_form_B
for i in range(len(list(seen))-1):
    listseen_GUIform_A.append(list(seen)[i][0])
    listseen_GUIform_B.append(list(seen)[i][1])

listseen_GUIform_A.append("全部")
listseen_GUIform_B.append("全部")
listseen_GUIform_A = list(set(listseen_GUIform_A)) #Checking A value is sole
listseen_GUIform_B = list(set(listseen_GUIform_B)) #Checking B value is sole



# test code
GUIform_extracted_data = []
n,s = input().split(" ")
for item in extracted_data_1:
    if item['ContractCode'] == n and item['Item' ]== s:
        GUIform_extracted_data.append(item)


# test code
GUIform_extracted_data = []
n,s = input().split(" ")
for item in extracted_data_1:
    if item['ContractCode'] == listseen_GUIform_A[listseen_GUIform_A.index(n)] and item['Item' ]== listseen_GUIform_B[listseen_GUIform_B.index(s)]:
        GUIform_extracted_data.append(item)


#數據整合
header_extracted_data = [data[len(data)-1]] + GUIform_extracted_data

#GUI輸出黨名稱
file_name = input()

with open(file_name+".csv","a",encoding="utf-8-sig",newline='') as d:

    #csv 宣告
    writer = csv.writer(d)

    #容器s"List s"
    s = []
    #容器x"List x"
    x = []

    #整理extracted_data_header總數據，提取目標數值並填入容器s"List s"
    for i in range(len(header_extracted_data)):
        for j in list(data[len(data)-1].keys()):
            rtt = f"{header_extracted_data[i][j]}"
            s.append(rtt)


    #整理容器s數據，提取目標數值並填入容器x"List x"
    for i in range(len(s)+1):
        if i!=0 and i%len(list(data[len(data)-1].keys()))==0:
            x.append(s[i-len(list(data[len(data)-1].keys())):i])

    #提取容器x目標數值並填入you_want.csv
    for i in x:
        writer.writerow(i)

#GUI 輸出檔案資料觀看處
print(f"{x[0]}\n{x[1]}")

#print(f"{x[0]}\n\n{x[1]}\n\n{x[2]}\n\n{x[3]}")'''



seen = set() #check title is sole
extracted_data_1 = [] #Correspond data about title
        
# GUIform_Alldata & GUIform_Alldata_Corresponddata
for item in data:
    key = (item['ContractCode'], item['Item'])
    if key[0]!='合約代碼' and key[1]!='項目':
        extracted_data_1.append(item)
        seen.add(key)

#(GUI_form_A & GUI_form_B)'s Options

listseen_GUIform_A = list()#GUI_form_A
listseen_GUIform_B = list()#GUI_form_B
for i in range(len(list(seen))-1):
    listseen_GUIform_A.append(list(seen)[i][0])
    listseen_GUIform_B.append(list(seen)[i][1])

listseen_GUIform_A.append("全部")
listseen_GUIform_B.append("全部")
listseen_GUIform_A = list(set(listseen_GUIform_A)) #Checking A value is sole
listseen_GUIform_B = list(set(listseen_GUIform_B)) #Checking B value is sole


GUIform_extracted_data = []

print(f"搜尋條件1: {listseen_GUIform_A}\n\n搜尋條件2: {listseen_GUIform_B}")

var_n = input("輸入第一個搜尋條件:")
var_s = input("輸入第二個搜尋條件:")

var_GUIform_A = listseen_GUIform_A[listseen_GUIform_A.index(var_n)]
var_GUIform_B = listseen_GUIform_B[listseen_GUIform_B.index(var_s)]

for item in extracted_data_1:
    #全資料
    if (var_GUIform_A == "全部" and item['ContractCode'] != var_GUIform_A) and (var_GUIform_B == "全部" and item['Item'] != var_GUIform_B):
        GUIform_extracted_data.append(item)
    #單一指定單輸出
    elif (var_GUIform_A != "全部" and item['ContractCode'] == var_GUIform_A) and (var_GUIform_B != "全部" and item['Item'] == var_GUIform_B):
        GUIform_extracted_data.append(item)
    #單一指定A多輸出
    elif (var_GUIform_A != "全部" and item['ContractCode'] == var_GUIform_A) and (var_GUIform_B == "全部" and item['Item'] != var_GUIform_B):
        GUIform_extracted_data.append(item)
    #單一指定B多輸出
    elif (var_GUIform_A == "全部" and item['ContractCode'] != var_GUIform_A) and (var_GUIform_B != "全部" and item['Item'] == var_GUIform_B):
        GUIform_extracted_data.append(item)

    #數據整合
header_extracted_data = [data[len(data)-1]] + GUIform_extracted_data

file_name = input("輸入匯出檔案名稱:")

with open(file_name+".csv","a",encoding="utf-8-sig",newline='') as d:

    #csv 宣告
    writer = csv.writer(d)

    #容器s"List s"
    s = []
    #容器x"List x"
    x = []

    #整理extracted_data_header總數據，提取目標數值並填入容器s"List s"
    for i in range(len(header_extracted_data)):
        for j in list(data[len(data)-1].keys()):
            rtt = f"{header_extracted_data[i][j]}"
            s.append(rtt)


    #整理容器s數據，提取目標數值並填入容器x"List x"
    for i in range(len(s)+1):
        if i!=0 and i%len(list(data[len(data)-1].keys()))==0:
            x.append(s[i-len(list(data[len(data)-1].keys())):i])

    #提取容器x目標數值並填入you_want.csv
    for i in x:
        writer.writerow(i)
