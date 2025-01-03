#chose_api_output

import Uesr_GUI_Function as urf
import tkinter as tk
import csv
from tkinter import ttk,simpledialog,messagebox
from Scatter_module import data_sort

save_output = set()
user_chose_output = list()
titlels = ["名稱","網址"]
chose_tree,y_chosescrollbar = None,None
chose,chose_commbo = None,None
            
def save_user_chose():
    global save_output,user_chose_output,chose,chose_commbo

    chose_api = urf.sa.extraction_orivalid_formatapi()

    if chose_commbo.get() in list(chose_commbo["values"]) or chose_commbo.get() != "":
        save_output.add(chose_commbo.get())
        list_saveoutput = data_sort(list(save_output))
        for x in list_saveoutput:
            user_chose_output.append([x,chose_api[list(chose_commbo["values"]).index(x)]])
        
        for e in range(len(user_chose_output)):
            user_chose_output[e] = tuple(user_chose_output[e])

        user_chose_output = set(user_chose_output)
        user_chose_output = list(user_chose_output)

            
    else:
        messagebox.showerror("錯誤","選項空白或不存在 !")


def clear_user_chose():

    if len(save_output) == 0:
        messagebox.showerror("錯誤","目前已清空")
    else:
        save_output.clear()
        user_chose_output.clear()
        messagebox.showinfo("成功","清除成功")


def outputcsv():
    global chose_commbo,user_chose_output

    if len(save_output) == 0 or chose_commbo.get() not in list(chose_commbo["values"]) or chose_commbo.get() == "":
        messagebox.showerror("錯誤","未登入任何資料 !")
    else:
        yaurname = simpledialog.askstring("匯出CSV", "請輸入匯出檔案名稱:")
        if yaurname == "" :
            messagebox.showerror("錯誤","檔案名稱不可空白 !")
        else:
            with open(yaurname+".csv","w+",encoding="utf-8-sig") as name:
                writer = csv.writer(name)
                writer.writerow(titlels)
                writer.writerows(user_chose_output)


def preview_chose():
    global chose_tree,y_chosescrollbar,titlels

    if len(save_output) == 0:
        messagebox.showerror("錯誤","請先選擇需要的API點選加入後，在使用預覽功能 !")
    else:
        if chose_tree is not None:
            chose_tree.destroy()
            y_chosescrollbar.destroy()

        chose_tree = ttk.Treeview(chose, columns = titlels, show='headings')  # Adjust columns as needed
        chose_tree.pack(fill=tk.BOTH, expand=True)
        y_chosescrollbar = ttk.Scrollbar(chose, orient="vertical", command=chose_tree.yview)
        y_chosescrollbar.pack(side = tk.RIGHT, fill='y')
                            
        for i in range(len(titlels)):  # Adjust number of columns as needed
            chose_tree.heading(i, text = titlels[i] , anchor='center')
            chose_tree.column(i, anchor='center')  # Center align the column headers
                                    
        for j in range(len(user_chose_output)):
            chose_tree.insert("","end",values = user_chose_output[j])

        '''if chose_tree.get_children():
            for i in range(len(chose_tree.get_children())):
                chose_tree.delete()'''
                

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
                            
        chose_tree.configure(yscrollcommand=y_chosescrollbar.set)


def close_newadd_gui():
    chose.destroy()


def newadd_gui():
    global chose_tree,y_chosescrollbar,chose,chose_commbo

    if urf.combo.get() == "":
        messagebox.showerror("錯誤","請選擇API開源網站 !")
    else:
        chose = tk.Tk()
        chose.title("匯出需求API")
        chose.geometry("500x500")

        chose_commbo = ttk.Combobox(chose,values = urf.sa.extraction_orivalid_chinesetitle())
        chose_commbo.pack()

        commbo_addframe = ttk.Frame(chose)
        commbo_addframe.pack(pady=10)

        addframe_button1 = ttk.Button(commbo_addframe, text="加入",command = save_user_chose)
        addframe_button1.pack(side=tk.LEFT, padx=5)

        addframe_button2 = ttk.Button(commbo_addframe, text="清空",command = clear_user_chose)
        addframe_button2.pack(side=tk.LEFT, padx=5)

        addframe_button3 = ttk.Button(commbo_addframe,text = "匯出csv",command = outputcsv)
        addframe_button3.pack(side=tk.LEFT, padx=5)

        addframe_button4 = ttk.Button(commbo_addframe, text="預覽選擇內容",command = preview_chose)
        addframe_button4.pack(side=tk.LEFT, padx=5)

        addframe_button4 = ttk.Button(commbo_addframe, text="關閉",command = close_newadd_gui)
        addframe_button4.pack(side=tk.LEFT, padx=5)

        chose_tree = ttk.Treeview(chose, columns = [], show='headings')  # Adjust columns as needed
        chose_tree.pack(fill=tk.BOTH, expand=True)
        y_chosescrollbar = ttk.Scrollbar(chose, orient="vertical", command=chose_tree.yview)
        y_chosescrollbar.pack(side = tk.RIGHT, fill='y')

        chose.mainloop()