
self = "https://openapi.taifex.com.tw"
#URL default 臺灣期貨交易所 OAS
def __init__(self):
    driver = None
    self = self

    if "https" not in self:
        raise ValueError("URL isn't legal.")
            
    #self.url = "https://openapi.taifex.com.tw"
    #self.url = "https://openapi.twse.com.tw"
        
def call_url(self):
    #self.url = url
    return self

        
def get_newurl(self,newurl):
    self = newurl
    return self
        
def crawl_url(self):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support.ui import Select

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get(self)
    crawl_url = driver.find_element(By.CLASS_NAME, "download-url-input").get_attribute("value")

    driver.quit()
        
    return crawl_url #json
        