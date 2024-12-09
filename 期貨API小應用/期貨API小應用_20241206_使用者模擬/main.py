import requests
import Scatter_module as sm

#self.url = "https://openapi.taifex.com.tw"
#self.url = "https://openapi.twse.com.tw"

url = sm.URL_Process()
sa = sm.Data_Process(url).all_url_data_fromload()
sa_key = list(sa.keys())
print(sa_key)





store = []
for i in range(len(sa_key)):

    url_I = sa[sa_key[i]]
    response_New = requests.get(url_I)
    if response_New.status_code == 200:
        data_New = response_New.json()
        store.append(list(data_New[0]))

set_store = set()

for i in store:
    set_store.add(tuple(i))

def Print_comparison_information(store,set_store):#列印對比資料
    with open ("see.txt","w",encoding = "utf-8-sig") as f:
        for i in store:
            i = str(i)
            i = i.replace("[","")
            i = i.replace("]","")
            i = i.replace(",","")
            f. write(str(i))
            f.write("\n")


    with open ("see_fire.txt","w",encoding = "utf-8-sig") as f:
        for i in set_store:
            i = str(i)
            i = i.replace("(","")
            i = i.replace(")","")
            i = i.replace(",","")
            f. write(str(i))
            f.write("\n")

    with open ("see.csv","w",encoding = "utf-8-sig") as f:
        for i in store:
            i = str(i)
            i = i.replace("[","")
            i = i.replace("]","")
            i = i.replace(",","")
            f. write(str(i))
            f.write("\n")

    with open ("see_fire.csv","w",encoding = "utf-8-sig") as f:
        for i in set_store:
            i = str(i)
            i = i.replace("(","")
            i = i.replace(")","")
            i = i.replace(",","")
            f. write(str(i))
            f.write("\n")