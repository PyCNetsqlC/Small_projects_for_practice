import URL_Process
import Data_Process


url = URL_Process.call_url()
sa = Data_Process(url).all_url_data_fromload()
sa_key = list(sa.keys())
print(sa_key)
