
#DESTINATION_URL_ONE = "https://openapi.taifex.com.tw"
#DESTINATION_URL_TEw = "https://openapi.twse.com.tw"

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from httpx import AsyncClient
import asyncio,nest_asyncio
import requests
import copy


#通用函式
def fetch_data(url:str)->list: #->list(dict) #抓取這個URL然後拋出該URL的json 
    session = requests.Session()
    session.headers.update({"Accept-Encoding": "gzip"})  # 啟用 gzip 壓縮
    response = session.get(url)
    if response.status_code == 200:
        data_api = response.json() 
    return data_api

    '''response = requests.get(url)
    if response.status_code == 200:
        data_api = response.json()
    return data_api'''


def better_fetch_data(better_url):#更新api請求功能
    async def better(better_url):
        async with AsyncClient() as response:
            reaway =  await response.get(better_url)
            return reaway.json()
    nest_asyncio.apply()
    return asyncio.run(better(better_url))


def save_data(data_api_text:list,data_chinese_title:list)->dict: # 所有api-url及api-url的中文標題
    data_fromload = dict(zip(data_api_text,data_chinese_title))
    return data_fromload


#主要使用在 Data_format_generation 類別
def extract_value(sort_dict:dict)->list:#篩出有效的api-url，並解析紀錄所有api內部的資料型態(API異常分類)
    api_store = []#所有有效的api
    store = []#所有api內部的資料型態
    problem_url = []#有問題的API網址會被紀錄在這裡
    for i in range(len(list(sort_dict.keys()))):
        try:
            #data_new = better_fetch_data(list(sort_dict.keys())[i])
            data_new = fetch_data(list(sort_dict.keys())[i])
            if len(data_new)==0:
                problem_url.append(list(sort_dict.keys())[i])
            else:
                api_store.append(list(sort_dict.keys())[i])
                store.append(list(data_new[0].keys()))
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


class UrlProcess:
    #The URL defaults to 臺灣期貨交易所 OAS
    def __init__(self,_url = "https://openapi.taifex.com.tw"):
        self._private_url = _url
        if "https" not in self._private_url:
            raise ValueError("URL isn't legal.")
    
    def call_url(self)->str:#確認目前抓取的目標網頁
        return self._private_url
    
    def get_new_url(self,new_url)->str:#可更新目標網頁
        self._private_url = new_url
        return self._private_url

    def crawl_url(self)->str:#抓取需要的資料網址
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(self._private_url)
        crawl_url_json = driver.find_element(By.CLASS_NAME, "download-url-input").get_attribute("value")
        driver.quit()
        return crawl_url_json #json


class DataComprehensive:#綜合資料
    def __init__(self,url_process:UrlProcess):
        self._url_process = url_process
        self._maindata = self._url_process.crawl_url()
        self._call_url = self._url_process.call_url()
    
    def call_data_url(self)->str:#確認抓取到的網址
        return self._maindata
    
    def alldata_fromload(self)->dict:
        def _parse_data_allapi_url(data_api:dict)->list: #抓取這網址拋出該URL所有api-url
            data_api_text = [f"{self._call_url}/v1"+i for i in list(data_api["paths"].keys())]  
            return data_api_text
        
        def _parse_data_allapi_chinesetitle(data_api:dict,data_api_text:list)->list: # 所有api-url的中文標題
            data_chinese_title = [(data_api["paths"][list(data_api["paths"].keys())[i]]["get"]["summary"]) for i in range(len(data_api_text))]
            return data_chinese_title

        #data_from = better_fetch_data(self._maindata)
        data_from = fetch_data(self._maindata)        
        data_api_url = _parse_data_allapi_url(data_from)#->list
        data_api_chinese = _parse_data_allapi_chinesetitle(data_from,data_api_url)#->list
        data_fromload = save_data(data_api_url,data_api_chinese)#->dict
        return data_fromload


class DataExtractionSort:
    def __init__(self,data_comprehensive:DataComprehensive):
        self._data_comprehensive = data_comprehensive
        self._apiurl_generation = self._data_comprehensive.alldata_fromload()
        self._orivalid_format = extract_value(self._apiurl_generation)
        self._filtered_format = data_sort(filter_unique_values(self._orivalid_format[0]))

    def extraction_allapiurl(self)->list: #生成原始資料api網址
        return list(self._apiurl_generation.keys())
    
    def extraction_allapichinesetitle(self)->list: #生成原始資料api網址的中文名稱
        return list(self._apiurl_generation.values())
    
    def extraction_orivalid_format(self)->list: #生成原始且有效,排序後資料型態
        return self._orivalid_format[0]
    
    def extraction_orivalid_formatapi(self)->list: #生成原始且有效,排序後api網址
        return self._orivalid_format[1]
    
    def extraction_orivalid_chinesetitle(self)->list:#生成原始且有效,排序後api網址的中文名稱
        def sence():#篩掉異常API
            for i in self._orivalid_format[2]:
                del try_find[i]

        try_find = copy.deepcopy(self._apiurl_generation)
        sence()
        try_find_list = list(try_find.values())        
        return try_find_list 

    def extraction_oriunvalid_api(self)->list: #生成原始且無效的api
        return self._orivalid_format[2]

    def extraction_filtered_format(self)->list: #生成唯一且有效,排序後資料型態(max->min)
        return self._filtered_format

    def extraction_filtered_formatapi(self)->list: #生成唯一且有效,排序後資料型態(max->min)
        filtered_formatapi = list(self._orivalid_format[1][self._orivalid_format[0].index(i)] for i in self._filtered_format)
        return filtered_formatapi
    

class DataGenerationTestdata:
    def __init__(self,extraction_sort:DataExtractionSort):
        self._extraction_sort = extraction_sort

    def generation_all(self):
        return save_data(self._extraction_sort.extraction_allapiurl(),self._extraction_sort.extraction_allapichinesetitle())
    
    def generation_orivail(self):
        return save_data(self._extraction_sort.extraction_orivalid_formatapi(),self._extraction_sort.extraction_orivalid_format())
    
    def generation_filtered(self):
        return save_data(self._extraction_sort.extraction_filtered_formatapi(),self._extraction_sort.extraction_filtered_format())
    