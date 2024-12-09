class URL_Process:

    #URL default 臺灣期貨交易所 OAS
    def __init__(self,url = "https://openapi.taifex.com.tw"):
        self.driver = None
        self.url = url

        if "https" not in self.url:
            raise ValueError("URL isn't legal.")
        
        #self.url = "https://openapi.taifex.com.tw"
        #self.url = "https://openapi.twse.com.tw"
    
    def call_url(self):
        #self.url = url
        return self.url

    
    def get_newurl(self,newurl):
        self.url = newurl
        return self.url
    
    def crawl_url(self):
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.support.ui import Select

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        driver.get(self.url)
        crawl_url = driver.find_element(By.CLASS_NAME, "download-url-input").get_attribute("value")

        driver.quit()
    
        return crawl_url #json
    

class Data_Process:
    
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
