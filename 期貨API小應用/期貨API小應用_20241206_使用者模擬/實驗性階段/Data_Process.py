import URL_Process

def __init__(self,url_process:URL_Process):

    self.url_process = url_process

            #output json
    self.main_url = self.url_process.crawl_url()
            
    #[if self.main_url.endswith(".json")] 提升易讀性
    if ".json" not in self.main_url:
        raise ValueError("Currently only json files are supported.")
            

def call_data_url(self):#,new_data):

    return self.main_url
            
        
def all_url_data_fromload(self):
    import requests

    response = requests.get(self.main_url)

    if response.status_code == 200:
        data_API = response.json()

                    #All data Key
        data_API_Key = list(data_API.keys())
                        
                    #API網址
        data_API_str = [f"{self.url_process.call_url()}/v1"+i for i in list(data_API["paths"].keys())]
                        
                    #API網址chinese title
        data_chinese_title = [(data_API["paths"][list(data_API["paths"].keys())[i]]["get"]["summary"]) for i in range(len(data_API_str))]
                        
                    #data_fromload = dict(zip(data_chinese_title : data_API_str)) str : str
        data_fromload = dict(zip(data_chinese_title,data_API_str))

    return data_fromload
