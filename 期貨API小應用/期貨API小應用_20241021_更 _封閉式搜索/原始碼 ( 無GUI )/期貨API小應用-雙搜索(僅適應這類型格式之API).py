'''

@待更新

# 自動抓取最新API，並獲取對應關鍵字，自動生成表單
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager#自動獲取最新版本
from selenium.webdriver.support.ui import Select,WebDriverWait # 使用 Select 對應下拉選單
from selenium.webdriver.support import expected_conditions as EC
import time

#獲取資料後，整理彙整輸出為符合使用者需求之資料檔
import requests
import json,csv
import copy


url = "https://openapi.taifex.com.tw/v1" #臺灣期貨交易所 

service = Service(ChromeDriverManager().install())  # 使用 webdriver-manager 自動獲取最新版本的 ChromeDriver

driver = webdriver.Chrome(service=service)  #啟動引擎

driver.get(url) #導入至此網址之網頁

time.sleep(5)   #預留網頁加載時間

# 獲取指定的 div 內容
#API_div = driver.find_element(By.CLASS_NAME, 'request-url')

API_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'request-url')))

pre_element = API_div.find_element(By.TAG_NAME, 'pre')
#content = rsi_div.get_attribute('outerHTML')
content = pre_element.text

print(content)


driver.quit()

'''






import requests
import json,csv
import copy

# API URL

#三大法人-區分各期貨契約-依日期
url_1 = "https://openapi.taifex.com.tw/v1/MarketDataOfMajorInstitutionalTradersDetailsOfFuturesContractsBytheDate" #適用雙索引
#三大法人-區分各期貨契約-依週別
url_2 = "https://openapi.taifex.com.tw/v1/MarketDataOfMajorInstitutionalTradersDetailsOfFuturesContractsBytheWeek" #適用雙索引
#三大法人-區分各選擇權契約-依日期
url_3 = "https://openapi.taifex.com.tw/v1/MarketDataOfMajorInstitutionalTradersDetailsOfOptionsContractsBytheDate"
#三大法人-區分各選擇權契約-依週別
url_4 = "https://openapi.taifex.com.tw/v1/MarketDataOfMajorInstitutionalTradersDetailsOfOptionsContractsBytheWeek"
#三大法人-選擇權買賣權分計-依日期
url_5 = "https://openapi.taifex.com.tw/v1/MarketDataOfMajorInstitutionalTradersDetailsOfCallsAndPutsBytheDate"
#三大法人-選擇權買賣權分計-依週別
url_6 = "https://openapi.taifex.com.tw/v1/MarketDataOfMajorInstitutionalTradersDetailsOfCallsAndPutsBytheWeek"

url_All = [url_1,url_2,url_3,url_4,url_5,url_6]
url_All_chTitle = ["日-區分各期貨契約","週-區分各期貨契約","日-區分各選擇權契約","週-區分各選擇權契約","日-選擇權買賣權分計","週-選擇權買賣權分計"]




# 發送 GET 請求
response = requests.get(url)

# 確認請求成功
if response.status_code == 200:
    # 將回應解析為 JSON
    data = response.json()
    #data的原始總資料
    original_data_all = [item for item in data] #or copy.deepcopy(data)
    # data's key
    data_key = list((data[0].keys()))

    #Chinese Title
    data_ch_title = ['日期', '合約代碼', '項目', '多單交易量', '多單交易值（千元）', '空單交易量', '空單交易值（千元）', '淨交易量', '淨交易值（千元）', '多單未平倉量', '多單未平倉合約價值（千元）', '空單未平倉量', '空單未平倉合約價值（千元）', '未平倉淨額', '未平倉合約淨值（千元）']
    
    # Title容器
    data_sort = dict()
    for i in range(len(data_key)-1):
        data_sort[data_key[i]] = data_ch_title[i]


else:
    print(f"Error: Unable to fetch data (status code: {response.status_code})")


def double_index(original_data_all,data_sort):
    seen = set() #check title is sole
    extracted_data_1 = [] #Correspond data about title
            
    # GUIform_Alldata & GUIform_Alldata_Corresponddata
    for item in original_data_all:
        key = (item["ContractCode"], item["Item"])
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

    var_n = input("輸入第一個搜尋條件:")#GUI
    var_s = input("輸入第二個搜尋條件:")#GUI

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

    header_extracted_data = [data_sort] + GUIform_extracted_data
    #容器x"List s"
    s = []
    #容器x"List x"
    x = []

    #整理extracted_data_header總數據，提取目標數值並填入容器s"List s"
    for i in range(len(header_extracted_data)):
        for j in list(header_extracted_data[0].keys()):
            rtt = f"{header_extracted_data[i][j]}"
            s.append(rtt)


    #整理容器s數據，提取目標數值並填入容器x"List x"
    for i in range(len(s)+1):
        if i!=0 and i%(len(list(data[len(data)-1].keys()))-1)==0:   #(len(list(data[len(data)-1].keys()))-1) == len(data_sort)
            x.append(s[i-(len(list(data[len(data)-1].keys()))-1):i])

    return x

x = double_index(original_data_all,data_sort)

file_name = input("輸入匯出檔案名稱:")#GUI

def CSV_Write(file_name,x):

    with open(file_name+".csv","a",encoding="utf-8-sig",newline='') as d:

        #csv 宣告
        writer = csv.writer(d)

        #提取容器x目標數值並填入you_want.csv
        for i in x:
            writer.writerow(i)

CSV_Write(file_name,x)