#測試資料

#self.url = "https://openapi.taifex.com.tw"
#self.url = "https://openapi.twse.com.tw"->第89筆資料有問題，抓不到

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.support.ui import Select
import requests



#通用函式
def fetch_data(url:str)->list: #->list(dict) #抓取這個URL然後拋出該URL的json 
    response = requests.get(url)
    if response.status_code == 200:
        data_API = response.json()
    return data_API

def save_data(data_API_str:list,data_chinese_title:list)->dict: # 所有api-url及api-url的中文標題
    data_fromload = dict(zip(data_API_str,data_chinese_title))
    return data_fromload

#主要使用在 Data_format_generation 類別
def extract_value(sort_dict:dict)->list:#篩出有效的api-url，並解析紀錄所有api內部的資料型態(API異常分類)
    api_store = []#所有有效的api
    store = []#所有api內部的資料型態
    problem_url = []#有問題的API網址會被紀錄在這裡
    for i in range(len(list(sort_dict.keys()))):
        try:
            data_New = fetch_data(list(sort_dict.keys())[i])
            if len(data_New)==0:
                problem_url.append(list(sort_dict.keys())[i])
            else:
                api_store.append(list(sort_dict.keys())[i])
                store.append(list(data_New[0].keys()))
        except:
            problem_url.append(list(sort_dict.keys())[i])
    return [store,api_store,problem_url]
    
def filter_unique_values(store:list)->list:#篩選唯一值，轉換串列內部資料型別。ex. set(tuple()) -> list(list()) '適用二維資料'
    set_store = set(tuple(i) for i in store)
    list_store = list(list(list(set_store)[i]) for i in range(len(set_store)))
    return list_store

def data_sort(list_store:list)->list:#氣泡排序，排序各API資料格式(多到少)
    for i in range(len(list_store)):
        for j in range(len(list_store)-1):
            if len(list_store[j]) < len(list_store[j+1]):
                list_store[j],list_store[j+1] = list_store[j+1],list_store[j]
    return list_store




class URL_Process:

    #The URL defaults to 臺灣期貨交易所 OAS
    def __init__(self,url = "https://openapi.taifex.com.tw"):
        self.url = url

        if "https" not in self.url:
            raise ValueError("URL isn't legal.")
    
    def call_url(self)->str:#確認目前抓取的目標網頁
        return self.url
    
    def get_newurl(self,newurl)->str:#可更新目標網頁
        self.url = newurl
        return self.url

    def crawl_url(self)->str:#抓取需要的資料網址
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(self.url)
        crawl_url = driver.find_element(By.CLASS_NAME, "download-url-input").get_attribute("value")
        driver.quit()
        return crawl_url #json


class Data_Comprehensive:#綜合資料
    
    def __init__(self,url_process:URL_Process):
        self.url_process = url_process
        self.maindata = self.url_process.crawl_url()
        self.call_url = self.url_process.call_url()
    
    def call_data_url(self)->str:#確認抓取到的網址
        return self.maindata
    
    def alldata_fromload(self)->dict:
        def parse_data_allapi_url(data_API:dict)->list: #抓取這網址拋出該URL所有api-url
            data_API_str = [f"{self.call_url}/v1"+i for i in list(data_API["paths"].keys())]  
            return data_API_str
        
        def parse_data_allapi_chinesetitle(data_API:dict,data_API_str:list)->list: # 所有api-url的中文標題
            data_chinese_title = [(data_API["paths"][list(data_API["paths"].keys())[i]]["get"]["summary"]) for i in range(len(data_API_str))]
            return data_chinese_title

        data_from = fetch_data(self.maindata)
        data_api_url = parse_data_allapi_url(data_from)#->list
        data_api_chinese = parse_data_allapi_chinesetitle(data_from,data_api_url)#->list
        data_fromload = save_data(data_api_url,data_api_chinese)#->dict

        return data_fromload


class Data_extraction_sort:
    def __init__(self,data_comprehensive:Data_Comprehensive):
        self.data_comprehensive = data_comprehensive
        self.apiurl_generation = self.data_comprehensive.alldata_fromload()
        self.orivalid_format = extract_value(self.apiurl_generation)
        self.filtered_format = data_sort(filter_unique_values(self.orivalid_format[0]))

    def extraction_allapiurl(self)->list: #生成原始資料api網址
        return list(self.apiurl_generation.keys())
    
    def extraction_allapichinesetitle(self)->list: #生成原始資料api網址的中文名稱
        return list(self.apiurl_generation.values())
    
    def extraction_orivalid_format(self)->list: #生成原始且有效,排序後資料型態
        return self.orivalid_format[0]
    
    def extraction_orivalid_formatapi(self)->list: #生成原始且有效,排序後資料型態
        return self.orivalid_format[1]
    
    def extraction_orivalid_chinesetitle(self)->list:#生成原始且有效,排序後api網址的中文名稱
        import copy
        try_find = copy.deepcopy(self.apiurl_generation)
        def sence():#篩掉異常API
            for i in self.orivalid_format[2]:
                del try_find[i]
        sence()
        try_find_list = list(try_find.values())        
        return try_find_list 

    def extraction_oriunvalid_api(self)->list: #生成原始且無效的api
        return self.orivalid_format[2]

    def extraction_filtered_format(self)->list: #生成唯一且有效,排序後資料型態(max->min)
        return self.filtered_format

    def extraction_filtered_formatapi(self)->list: #生成唯一且有效,排序後資料型態(max->min)
        filtered_formatapi = list(self.orivalid_format[1][self.orivalid_format[0].index(i)] for i in self.filtered_format)
        return filtered_formatapi
    


class Data_generation_testdata:
    def __init__(self,extraction_sort:Data_extraction_sort):
        self.extraction_sort = extraction_sort

    def generation_all(self):
        return save_data(self.extraction_sort.extraction_allapiurl(),self.extraction_sort.extraction_allapichinesetitle())
    
    def generation_orivail(self):
        return save_data(self.extraction_sort.extraction_orivalid_formatapi(),self.extraction_sort.extraction_orivalid_format())
    
    def generation_filtered(self):
        return save_data(self.extraction_sort.extraction_filtered_formatapi(),self.extraction_sort.extraction_filtered_format())
    