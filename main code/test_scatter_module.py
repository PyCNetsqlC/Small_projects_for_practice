#測試資料

#self.url = "https://openapi.taifex.com.tw"
#self.url = "https://openapi.twse.com.tw"->第89筆資料有問題，抓不到




import pytest
from Scatter_module import *


@pytest.mark.parametrize(("ori_url","new_url"),
    [
    ("https://openapi.taifex.com.tw","https://openapi.twse.com.tw"),
    ("https://openapi.twse.com.tw","https://openapi.taifex.com.tw"),
    ("https://exam.csf.org.tw/examinee/","https://www.codejudger.com/")
    ])
# 測試 get_newurl 方法
def test_get_newurl(ori_url,new_url):
    url_process = URL_Process(ori_url)
    n_new_url = url_process.get_newurl(new_url)
    assert n_new_url == new_url

# 測試 crawl_url 方法 (這是一個需要執行 Web 驅動的測試)
@pytest.mark.parametrize(("url", "expected"), 
    [
    ("https://openapi.twse.com.tw", "https://openapi.twse.com.tw/v1/swagger.json"),
    ("https://openapi.taifex.com.tw","https://openapi.taifex.com.tw/v1/swagger.json")  # 假設返回這個 URL
    ])
def test_crawl_url(url:str, expected:str):
    url_process = URL_Process(url)
    crawled_url = url_process.crawl_url()

    if "/v1" not in crawled_url:
        find_v1 = crawled_url.find("/swagger.json")
        crawled_url = crawled_url[:find_v1] + "/v1" + crawled_url[find_v1:]
        
    assert crawled_url == expected



@pytest.mark.parametrize(("url", "text"), 
    [
    ("https://openapi.taifex.com.tw",'店頭集中結算會員名冊'),
    ("https://openapi.twse.com.tw",'上市公司企業ESG資訊揭露彙總資料-反競爭行為法律訴訟') # 假設返回這個 URL
    ])

# 測試 Data_Process 類別
def test_data_process(url:str,text:str):
    url_process = URL_Process(url)
    data_comprehensive = Data_Comprehensive(url_process = url_process)
    data = data_comprehensive.alldata_fromload()  # 這會測試從 API 加載資料
    assert list(data.values())[0] == text
    #assert len(data) > 0, "Data should not be empty"


@pytest.mark.parametrize(("url", "expected","try_third"), 
    [
    ("https://openapi.twse.com.tw","https://openapi.taifex.com.tw/v1/swagger.json","https://openapi.taifex.com.tw"),
    ("https://openapi.taifex.com.tw","https://openapi.twse.com.tw/v1/swagger.json","https://openapi.twse.com.tw")  # 假設返回這個 URL
    ])

def test_comprehensive(url,expected,try_third):

    try_url = URL_Process(url)
    try_url.get_newurl(try_third)
    try_call_url = try_url.call_url()
    sa = Data_Comprehensive(try_url).call_data_url()

    if "/v1" not in sa:
        find_v1 = sa.find("/swagger.json")
        sa = sa[:find_v1] + "/v1" + sa[find_v1:]

    assert try_call_url == try_third
    assert try_url != try_call_url
    assert sa == expected

refail = ["https://openapi.twse.com.tw","https://openapi.taifex.com.tw"]

test_data = refail[0]

@pytest.mark.parametrize("testurl",[test_data])

def test_twse_com(testurl):

    url = URL_Process(testurl)
    sd = Data_Comprehensive(url)
    sa = Data_extraction_sort(sd)

    ffc = extract_value(sd.alldata_fromload())

    assert len(ffc[0]) == 140
    assert len(ffc[1]) == 4
