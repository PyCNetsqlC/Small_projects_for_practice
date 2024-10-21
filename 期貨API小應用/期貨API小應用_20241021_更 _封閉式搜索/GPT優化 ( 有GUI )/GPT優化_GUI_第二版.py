import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import requests
import csv

# API URLs
url_1 = "https://openapi.taifex.com.tw/v1/MarketDataOfMajorInstitutionalTradersDetailsOfFuturesContractsBytheDate"
url_2 = "https://openapi.taifex.com.tw/v1/MarketDataOfMajorInstitutionalTradersDetailsOfFuturesContractsBytheWeek"
url_3 = "https://openapi.taifex.com.tw/v1/MarketDataOfMajorInstitutionalTradersDetailsOfOptionsContractsBytheDate"
url_4 = "https://openapi.taifex.com.tw/v1/MarketDataOfMajorInstitutionalTradersDetailsOfOptionsContractsBytheWeek"
url_5 = "https://openapi.taifex.com.tw/v1/MarketDataOfMajorInstitutionalTradersDetailsOfCallsAndPutsBytheDate"
url_6 = "https://openapi.taifex.com.tw/v1/MarketDataOfMajorInstitutionalTradersDetailsOfCallsAndPutsBytheWeek"

url_All = [url_1, url_2, url_3, url_4, url_5, url_6]
url_All_chTitle = ["日-區分各期貨契約", "週-區分各期貨契約", "日-區分各選擇權契約", "週-區分各選擇權契約", "日-選擇權買賣權分計", "週-選擇權買賣權分計"]

# Fetch data based on selected API URL
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: Unable to fetch data (status code: {response.status_code})")
        return None

# Update data based on selected API URL
def on_select(event):
    chosen_index = url_All_chTitle.index(combo.get())
    selected_url = url_All[chosen_index]
    global original_data_all
    original_data_all = fetch_data(selected_url)

    if original_data_all:
        # Extract unique values for ContractCode and Item
        options_A = list(set(item["ContractCode"] for item in original_data_all)) + ["全部"]
        options_B = list(set(item["Item"] for item in original_data_all)) + ["全部"]

        # Update combo boxes
        combo_A['values'] = options_A
        combo_B['values'] = options_B

# Filter data based on user selections
def filter_data():
    var_n = combo_A.get()
    var_s = combo_B.get()
    if original_data_all:
        result = double_index(original_data_all, var_n, var_s)
        print(result)
        return result

# Function to filter data based on criteria
def double_index(original_data_all, var_GUIform_A, var_GUIform_B):
    extracted_data = []
    for item in original_data_all:
        if (var_GUIform_A == "全部" or item['ContractCode'] == var_GUIform_A) and (var_GUIform_B == "全部" or item['Item'] == var_GUIform_B):
            extracted_data.append(item)
    return extracted_data

# Function to write filtered data to a CSV file
def CSV_Write(file_name, data):
    with open(file_name + ".csv", "a", encoding="utf-8-sig", newline='') as d:
        writer = csv.writer(d)
        # Write header if data is not empty
        if data:
            header = data[0].keys()
            writer.writerow(header)
            for row in data:
                writer.writerow(row.values())

# Handle CSV export
def export_to_csv():
    filtered_data = filter_data()
    if filtered_data:
        file_name = simpledialog.askstring("輸出檔案名稱", "請輸入匯出檔案名稱:")
        if file_name:
            CSV_Write(file_name, filtered_data)
            print(f"{file_name}.csv 已匯出。")

# Create the GUI
def create_gui():
    global combo_A, combo_B, combo

    root = tk.Tk()
    root.title("期貨API串接應用小專案")
    root.geometry("400x300")  # Set a default size for the window

    # 下拉選單：選擇 API 查詢條件
    label = ttk.Label(root, text="三大法人查詢條件:")
    label.pack()

    combo = ttk.Combobox(root, values=url_All_chTitle)
    combo.pack()
    combo.bind("<<ComboboxSelected>>", on_select)

    # 下拉選單A
    label_A = ttk.Label(root, text="搜尋條件1:")
    label_A.pack()
    combo_A = ttk.Combobox(root)
    combo_A.pack()

    # 下拉選單B
    label_B = ttk.Label(root, text="搜尋條件2:")
    label_B.pack()
    combo_B = ttk.Combobox(root)
    combo_B.pack()

    # Create a frame for buttons
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)

    # 按鈕：篩選
    filter_button = ttk.Button(button_frame, text="查詢", command=filter_data)
    filter_button.pack(side=tk.LEFT, padx=5)

    # 按鈕：匯出 CSV
    export_button = ttk.Button(button_frame, text="匯出 CSV", command=export_to_csv)
    export_button.pack(side=tk.LEFT, padx=5)

    root.mainloop()

# 主執行
original_data_all = None
create_gui()
