import Scatter_module as sc

def key_fromload(callurl:str)->tuple:#不可改動，篩選資料關鍵字。(除非你要抓自己的資料關鍵字)
    if "taifex.com" in callurl:
        keyword_fromload = ("TypeOfTheUnderlyingSecurity","Contracts","Products","ProductCode","Item","ContractCode","ContractType","StockName","FCMName","ContractName","Contract","YYYYMM","Date")
    elif "twse.com" in callurl:
        keyword_fromload = ()
    return keyword_fromload



def internal_keyword(keyfromload:tuple,apiurl:str,till:list):

    apidata = sc.fetch_data(apiurl)
    apidata_format = list(apidata[0].keys())

    api_data_key = set()#自動生成搜尋條件表單

    if apidata_format in till:
        for i in keyfromload:
            if i in apidata_format:
                keyword = i
                api_data_key.add("all")
                break
        for g in range(len(apidata)):
            api_data_key.add(apidata[g][keyword])

    api_data_key = sc.data_sort(list(api_data_key))

    return [keyword,apidata,apidata_format,api_data_key]



def internal_values(keyword,apidata,apidata_format,string):

    api_data_item = list()#登錄與搜尋條件相應的資料
    api_data_item.append(apidata_format)#表頭

    for j in range(len(apidata)):
        if  string == "all":
            api_data_item.append(list(apidata[j].values()))
        elif string != "all" and apidata[j][keyword] == string:
            api_data_item.append(list(apidata[j].values()))
        
    return api_data_item
    








