from scatter_module import better_fetch_data,data_sort,fetch_data
import pandas as pd

def key_fromload(callurl:str)->tuple:#不可改動，篩選資料關鍵字。(除非你要抓自己的資料關鍵字)
    if "taifex.com" in callurl:
        keyword_fromload = ("TypeOfTheUnderlyingSecurity","Contracts","Products","ProductCode","Item","ContractCode","ContractType","StockName","FCMName","ContractName","Contract","Name","YYYYMM","Date")
    elif "twse.com" in callurl:
        keyword_fromload = ('TWSECode','IndustryCat','指數','Time','股票代號','Month','STOCKsName','No','Date','Name','Code','出表日期')
    return keyword_fromload


'''
#原版
#進階debug keyword "YYYYMM" & "Date" ， 排序問題解決 ， 部分資料無法避免重複
def internal_keyword(keyfromload:tuple,apiurl:str,till:list)->list[list,list,set,list]:
    apidata = better_fetch_data(apiurl)
    #apidata = fetch_data(apiurl)
    apidata_format = list(apidata[0].keys())
    api_data_key = list()#自動生成搜尋條件表單
    if apidata_format in till:
        for i in keyfromload:
            if i in apidata_format:
                keyword = i
                break

    try:#期貨所的邏輯
        if keyword == "YYYYMM" or keyword == "Date":
            for g in range(len(apidata)):
                if apidata[g][keyword] not in api_data_key:
                    api_data_key.append(apidata[g][keyword])
                else:
                    pass
            api_data_key.append("all")
        else:
            api_data_key.append("all")
            for g in range(len(apidata)):
                api_data_key.append(apidata[g][keyword])
            api_data_key = data_sort(list(set(api_data_key)))
    
    except:
            api_data_key.append("all")
            for g in range(len(apidata)):
                api_data_key.append(apidata[g][keyword])

    return [keyword,apidata,apidata_format,api_data_key]
'''


#混和模式第一版型
def internal_keyword(keyfromload:tuple,apiurl:str,till:list)->list[list,list,set,list]:
    apidata = better_fetch_data(apiurl)
    #apidata = fetch_data(apiurl)
    apidata_format = list(apidata[0].keys())
    api_data_key = list()#自動生成搜尋條件表單
    if apidata_format in till:
        for i in keyfromload:
            if i in apidata_format:
                keyword = i
                break

    try:#期貨所的邏輯
        if keyword == "YYYYMM" or keyword == "Date":
            for g in range(len(apidata)):
                if apidata[g][keyword] not in api_data_key:
                    api_data_key.append(apidata[g][keyword])
                else:
                    pass
            api_data_key.append("all")
        else:
            api_data_key.append("all")
            for g in range(len(apidata)):
                api_data_key.append(apidata[g][keyword])
            api_data_key = data_sort(list(set(api_data_key)))
    
    except:#證交所的邏輯
        try:
            api_data_key.append("all")
            for g in range(len(apidata)):
                api_data_key.append(apidata[g][keyword])
            api_data_key = data_sort(list(set(api_data_key)))
        except:
            api_data_key.append("all")
            for g in range(len(apidata)):
                api_data_key.append(apidata[g][keyword])

    return [keyword,apidata,apidata_format,api_data_key]


'''
#混和模式第二版型(改良中)
def internal_keyword(keyfromload:tuple,apiurl:str,till:list)->list[list,list,set,list]:
    try:#期貨所的邏輯
        apidata = better_fetch_data(apiurl)
        #apidata = fetch_data(apiurl)
        apidata_format = list(apidata[0].keys())
        api_data_key = list()#自動生成搜尋條件表單
        if apidata_format in till:
            for i in keyfromload:
                if i in apidata_format:
                    keyword = i
                    break
        if keyword == "YYYYMM" or keyword == "Date":
            for g in range(len(apidata)):
                if apidata[keyword] not in api_data_key:
                    api_data_key.append(apidata[keyword])
                else:
                    pass
            api_data_key.append("all")
        else:
            api_data_key.append("all")
            for g in range(len(apidata)):
                api_data_key.append(apidata[keyword])
            api_data_key = data_sort(list(set(api_data_key)))
    
    except:#證交所的邏輯
        apidata = pd.read_json(apiurl)#改良處
        apidata_format = list(apidata.keys())
        api_data_key = list()#自動生成搜尋條件表單
        if apidata_format in till:
            for i in keyfromload:
                if i in apidata_format:
                    keyword = i
                    break
        try:
            for g in range(len(apidata)):
                api_data_key.append(list(apidata[keyword])[g])
            api_data_key.append("all")
            api_data_key = data_sort(list(set(api_data_key)))
        except:
            for g in range(len(apidata)):
                api_data_key.append(list(apidata[keyword])[g])
            api_data_key.append("all")

    return [keyword,apidata,apidata_format,api_data_key]
'''


#混和模式第一版型
def internal_values(keyword:str,apidata:dict,apidata_format:list,apitext:str)->list:
    api_data_item = list()#登錄與搜尋條件相應的資料
    api_data_item.append(apidata_format)#表頭
    for j in range(len(apidata)):
        if  apidata[j][keyword] == apitext and apitext != "all":
            api_data_item.append(list(apidata[j].values()))
        elif apitext == "all":
            api_data_item.append(list(apidata[j].values())) 
    return api_data_item


'''混和模式第二版型(改良中)
#改良證交所的邏輯中
def internal_values(api_data_key:list,apidata:dict,apidata_format:list,apitext:str)->list:
    api_data_item = list()#登錄與搜尋條件相應的資料
    api_data_item.append(apidata_format)#表頭
    if apitext in api_data_key:
        for j in list(apidata.values):
            if  apitext in j and apitext != "all":
                api_data_item.append(list(j))
            elif apitext == "all":
                api_data_item.append(list(j))
        return api_data_item
''' 





