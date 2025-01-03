
#臺灣證券交易所 OpenAPI 網址 建構中處理資料集程式碼
#https://openapi.twse.com.tw 建構中處理資料集程式碼
#self.url = "https://openapi.twse.com.tw"->第89筆資料有問題，抓不到/第81筆沒有資料/第101筆資料顯示不出/第93、106筆尚未釐清原因



import requests

def fetch_data(url:str)->dict: # 抓取這個URL然後拋出該URL的json 
    response = requests.get(url)
    if response.status_code == 200:
        data_API = response.json()    
    return data_API
    
def parse_data_allapi_url(data_API:dict,data:str)->list: #抓取這個拋出該URL所有api-url
    data_API_str = [f"{data}/v1"+i for i in list(data_API["paths"].keys())]  
    return data_API_str

def parse_data_allapi_chinesetitle(data_API:dict,data_API_str:list)->list: # 所有api-url的中文標題
    data_chinese_title = [(data_API["paths"][list(data_API["paths"].keys())[i]]["get"]["summary"]) for i in range(len(data_API_str))]
    return data_chinese_title

def save_data(data_API_str:list,data_chinese_title:list)->dict: # 所有api-url及api-url的中文標題
    data_fromload = dict(zip(data_API_str,data_chinese_title))
    return data_fromload

def extract_value(sort_dict:dict)->list:#所有api-url的所有資料型態
    store = []
    fnn = []
    for i in range(len(list(sort_dict.keys()))):
        try:
            data_New = fetch_data(list(sort_dict.keys())[i])
            if len(data_New)==0:
                print("Content is null.")
                #fnn.append(f"Content is null: {i}")
                fnn.append(list(sort_dict.keys())[i])
            else:
                store.append(list(data_New[0].keys()))
        except:
                print("URL can't find.")
                #fnn.append(f"URL has problem: {i}")
                fnn.append(list(sort_dict.keys())[i])
    return [fnn,store]

'''def extract_value(sort_dict:dict)->list:#所有api-url的所有資料型態
    store = []
    fnn = []
    for i in range(len(list(sort_dict.values()))):
        
        data_New = fetch_data(list(sort_dict.values())[i])
        if len(data_New)==0:
            print("Content is null.")
            #fnn.append(f"Content is null: {i}")
            fnn.append(list(sort_dict.values())[i])
        else:
            store.append(list(data_New[0].keys()))
    return [fnn,store]'''



qc = "https://openapi.twse.com.tw"
qe = fetch_data("https://openapi.twse.com.tw/v1/swagger.json")
qx = parse_data_allapi_url(qe,qc)
qr = parse_data_allapi_chinesetitle(qe,qx)
qall = save_data(qx,qr)

qex = extract_value(qall)
len(qex[0])
len(qall)

extract = extract_value(qall)[0]
for i in extract:
    del qall[i]


del qall["上市公司企業ESG資訊揭露彙總資料-食品安全"]
del qall["上市公司每日內部人持股轉讓事前申報表-持股未轉讓日報表"]
del qall["上市公司 103 年應編製與申報 CSR 報告書名單"]
del qall["上市公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更停止買賣公司"]
del qall["上市公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更列為變更交易公司"]


len(qx)
len(qr)


del qx[92]
del qx[88]
qx[81]
qx[89]
qx[94]
qx[102]
qx[107]
del qr[102]
del qr[88]
qr[81]#上市公司每日內部人持股轉讓事前申報表-持股未轉讓日報表
qr[89]#上市公司 103 年應編製與申報 CSR 報告書名單
qr[94]#上市認購(售)權證每日成交資料檔
qr[102]#上市公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更停止買賣公司
qr[107]#上市公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更列為變更交易公司



#網站資料更新 2024/12/22

8/92/100/113/118

qx[8]
qx[92]
qx[100]
qx[105]
qx[113]
qx[118]

qr[8]#'上市公司企業ESG資訊揭露彙總資料-食品安全'
qr[92]#'上市公司每日內部人持股轉讓事前申報表-持股未轉讓日報表'
qr[100]#'上市公司 103 年應編製與申報 CSR 報告書名單'
qr[105]#'上市認購(售)權證每日成交資料檔'
qr[113]#'上市公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更停止買賣公司'
qr[118]#'上市公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更列為變更交易公司'


stron= []
x = 0
#if url == "https://openapi.twse.com.tw":
#def twse_only():
for i in range(len(qall)):
    ert = fetch_data(list(qall.values())[i])
    stron.append(list(ert[0].keys()))
for i in range(9,len(qr)):
    ert = fetch_data(qx[i])
    stron.append(list(ert[0].keys()))
    #stron.append(ert)

for i in range(len(qr)):
    if i==92:
        ert1 = fetch_data(qx[92])
        stron.append(ert1)
        print(i)
    elif i==100:
        ert2 = fetch_data(qx[100])
        stron.append(ert2)
        print(i)
    elif i==105:
        ert3 = fetch_data(qx[105])
        stron.append(ert3)
        print(i)
    else:
        ert = fetch_data(qx[i])
        stron.append(ert)


ert = fetch_data(qx[89])


len(stron)

stron[105]
stron[92]

ws = []
for i in range(len(stron)):
    ws.append(len(stron[i]))
for i in range(90,len(stron)):
    if len(stron[i]) == 0:
        ws.append(f"{i}:null")

qx[81]
qx[92]
qx[101]
qx[106]

qr[81]
qr[93]
qr[101]
qr[106]



z = fetch_data('https://openapi.twse.com.tw/v1/brokerService/secRegData')

ddd = []
ee = fetch_data(qx[101])
ddd.append(ee)

ws[81]
ws[93]
ws[101]
ws[106]


def alldata_fromload(self)->dict:





    url = self.url_process.call_url()#-> str
    data = fetch_data(self.url_process.crawl_url())#-> dict
    data_api_url = parse_data_allapi_url(data,url)#->list

        #臺灣證券交易所 OpenAPI的api補丁
        #if url == 'https://openapi.twse.com.tw' and data_api_url[data_api_url.index('https://openapi.twse.com.tw/v1/static/20151104/CSR103')] == 'https://openapi.twse.com.tw/v1/static/20151104/CSR103':
        #    del data_api_url[data_api_url.index('https://openapi.twse.com.tw/v1/static/20151104/CSR103')]
        
    data_api_chinese = parse_data_allapi_chinesetitle(data,data_api_url)#->list
        
        #臺灣證券交易所 OpenAPI的api補丁
        #if url == 'https://openapi.twse.com.tw' and data_api_chinese[data_api_chinese.index('上市公司 103 年應編製與申報 CSR 報告書名單')] == '上市公司 103 年應編製與申報 CSR 報告書名單':
        #    del data_api_chinese[data_api_chinese.index('上市公司 103 年應編製與申報 CSR 報告書名單')]
        
    data_fromload = save_data(data_api_chinese,data_api_url)#->dict
        
    return data_fromload 