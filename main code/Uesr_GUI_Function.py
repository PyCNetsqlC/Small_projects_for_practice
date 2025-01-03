#Uesr_GUI_Function

from tkinter import ttk,simpledialog,messagebox
from Scatter_module import URL_Process,Data_Comprehensive,Data_extraction_sort
from Chose_api_output import newadd_gui,close_newadd_gui
import tkinter as tk
import API_internal_data_processing as ap
import csv as csv

#commbox
url = None
sd = None
sa = None
keyfromload = None

#commbox_A
apidatakey = None
sortdata = None
varstr = "all"

#commbox_B
combob_list = []
tree = None
x_scrollbar = None
y_scrollbar = None


#GUI 
root = None

label = None
combo = None

label_A = None
combo_A = None 

label_B = None
combo_B = None

button_frame = None
filter_button = None


def commbox(side):
    global url,sd,sa,keyfromload

    if combo.get() == "期貨所":
        website = "https://openapi.taifex.com.tw"

    elif combo.get() == "證交所":
        website = "https://openapi.twse.com.tw"
        
    if website:

        keyfromload = ap.key_fromload(website)
        url = URL_Process(website)
        sd = Data_Comprehensive(url)
        sa = Data_extraction_sort(sd)
        combo_A["values"] = sa.extraction_orivalid_chinesetitle()
        

def commbox_A(commbox_a_side):
    global apidatakey,sortdata,combob_list,tree,x_scrollbar,y_scrollbar,varstr

    combo_A_api = sa.extraction_orivalid_formatapi()
    apiurl = combo_A_api[list(combo_A["values"]).index(combo_A.get())]    
    apidatakey = ap.internal_keyword(keyfromload,apiurl,sa.extraction_orivalid_format())
    sortdata = ap.internal_values(apidatakey[0],apidatakey[1],apidatakey[2],varstr)
    combo_B["values"] = list(apidatakey[3])

    combob_list = apidatakey[2]
    
    if tree is not None:
        tree.destroy()
        x_scrollbar.destroy()
        y_scrollbar.destroy()
    
    tree = ttk.Treeview(root, columns = combob_list, show='headings')  # Adjust columns as needed
    tree.pack(fill=tk.BOTH, expand=True)

    for i in range(len(combob_list)):  # Adjust number of columns as needed
        tree.heading(i, text=combob_list[i], anchor='center')
        tree.column(i, anchor='center')  # Center align the column headers
    
    for j in range(1,len(sortdata)):
        tree.insert("","end",values = sortdata[j])

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
    
    x_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
    x_scrollbar.pack(side = tk.BOTTOM, fill=tk.X)
    y_scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    y_scrollbar.pack(side = tk.RIGHT, fill='y')

    tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
    

def commbox_B(commbox_b_side):
    global varstr

    varstr = combo_B.get()
    commbox_A(commbox_b_side)


def csv_output():
    if combo_A.get() == "":
        messagebox.showerror("錯誤","請選擇站內API !")
    else:
        global sortdata

        file_name = simpledialog.askstring("匯出CSV", "請輸入匯出檔案名稱:")

        if file_name == "":
                messagebox.showerror("錯誤","檔案名稱不可空白 !")
        else:
            with open(file_name + ".csv","w+",encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerows(sortdata)

def close_create_gui():
    root.destroy()
    close_newadd_gui()

def create_gui():
    global root,label,combo,label_A,combo_A,label_B,combo_B,button_frame,filter_button
    global tree,x_scrollbar,y_scrollbar

    combob_list = []

    root = tk.Tk()
    root.title("Test User GUI")
    root.geometry("600x400")  # Set a default size for the window

    label = tk.Label(root, text="選擇API開源網站:")
    label.pack()
    combo = ttk.Combobox(root)
    combo.pack()
    combo["values"] = ["期貨所","證交所"]
    combo.bind("<<ComboboxSelected>>", commbox)

    label_A = ttk.Label(root, text="選擇站內API:")
    label_A.pack()
    combo_A = ttk.Combobox(root)
    combo_A.pack()
    combo_A.bind("<<ComboboxSelected>>", commbox_A)

    label_B = ttk.Label(root, text="輔助搜索:")
    label_B.pack()
    combo_B = ttk.Combobox(root)
    combo_B.pack()
    combo_B.bind("<<ComboboxSelected>>", commbox_B)

    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)
    filter_button1 = ttk.Button(button_frame, text="匯出CSV",command = csv_output)
    filter_button1.pack(side=tk.LEFT, padx=5)
    filter_button2 = ttk.Button(button_frame, text="匯出需求API",command = newadd_gui)
    filter_button2.pack(side=tk.LEFT, padx=5)
    filter_button3 = ttk.Button(button_frame, text="關閉",command = close_create_gui)
    filter_button3.pack(side=tk.LEFT, padx=5)

    tree = ttk.Treeview(root, columns = combob_list, show='headings')  # Adjust columns as needed
    tree.pack(fill=tk.BOTH, expand=True)

    x_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
    x_scrollbar.pack(side = tk.BOTTOM, fill=tk.X)
    y_scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    y_scrollbar.pack(side = tk.RIGHT, fill='y')

    tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

    root.mainloop()


    

    



    
