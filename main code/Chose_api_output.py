from tkinter import ttk,simpledialog,messagebox
import uesr_gui_function as ugf
from scatter_module import data_sort
import tkinter as tk
import csv


save_output = list()
user_chose_output = list()
titlels = ["名稱","網址"]
chose_tree,y_chosescrollbar = None,None
chose,chose_commbo = None,None
offoron = 0


def chose_return_default():
    global save_output,user_chose_output,titlels
    global chose_tree,y_chosescrollbar,chose_commbo 
    global offoron

    save_output = list()
    user_chose_output = list()
    titlels = ["名稱","網址"]
    chose_tree,y_chosescrollbar = None,None
    chose_commbo = None
    offoron = 0


def update_form():
    global chose_tree,y_chosescrollbar,titlels
    if chose_tree is not None:
        chose_tree.destroy()
        y_chosescrollbar.destroy()

    chose_tree = ttk.Treeview( chose , columns = titlels, show = 'headings' )  # Adjust columns as needed
    chose_tree.pack( fill = tk.BOTH , expand = True )
    y_chosescrollbar = ttk.Scrollbar( chose , orient = "vertical" , command = chose_tree.yview )
    y_chosescrollbar.pack( side = tk.RIGHT , fill = 'y' )
                                
    for i in range(len(titlels)):
        chose_tree.heading( i , text = titlels[i] , anchor = 'center' )
        chose_tree.column( i , anchor = 'center' )  
                                        
    for j in range(len(user_chose_output)):
        chose_tree.insert( "" , "end" , values = user_chose_output[j] )

    style = ttk.Style()
    style.configure( "Treeview.Heading" , font = ("Arial", 10, "bold") )                
    chose_tree.configure(  yscrollcommand = y_chosescrollbar.set )


def save_user_chose():
    global save_output,user_chose_output,chose,chose_commbo
    if chose_commbo.get() in list(chose_commbo["values"])  or  chose_commbo.get() != "":
        if chose_commbo.get() not in save_output:
            user_chose_output.clear()
            save_output.append(chose_commbo.get())
            save_output = set(save_output)
            save_output = data_sort( list(save_output) )
            chose_api = ugf.sa.extraction_orivalid_formatapi()
            
            for x in save_output:
                user_chose_output.append( [ x , chose_api[list(chose_commbo["values"]).index(x)] ] )

            update_form()
        else:
            messagebox.showerror( "錯誤" , "選項已存在 !" )
    else:
        messagebox.showerror( "錯誤" , "選項空白或不存在 !" )


def clear_user_chose():
    if len(save_output) == 0:
        messagebox.showerror( "錯誤" , "目前已清空" )
    else:
        save_output.clear()
        user_chose_output.clear()
        update_form()
        messagebox.showinfo( "成功" , "清除成功" )


def output_csv():
    global chose_commbo,user_chose_output
    if len(save_output) == 0  or  chose_commbo.get() not in list(chose_commbo["values"])  or  chose_commbo.get() == "":
        messagebox.showerror( "錯誤" , "未登入任何資料 !" )
    else:
        yaurname = simpledialog.askstring( "匯出CSV" , "請輸入匯出檔案名稱:" )
        try:
            if yaurname == "" :
                messagebox.showerror( "錯誤" , "檔案名稱不可空白 !" )
            else:
                with open( yaurname + ".csv" , "w+" , encoding = "utf-8-sig" ) as name:
                    writer = csv.writer(name)
                    writer.writerow(titlels)
                    writer.writerows(user_chose_output)
                    messagebox.showinfo("成功","匯出成功 !")
        except:
            messagebox.showerror("錯誤","檔案名稱不合法 !")


def output_txt():
    global chose_commbo,user_chose_output
    if len(save_output) == 0  or  chose_commbo.get() not in list(chose_commbo["values"])  or  chose_commbo.get() == "":
        messagebox.showerror( "錯誤" , "未登入任何資料 !" )
    else:
        yaurname = simpledialog.askstring( "匯出TXT" , "請輸入匯出檔案名稱:" )
        try:
            if yaurname == "" :
                messagebox.showerror( "錯誤" , "檔案名稱不可空白 !" )
            else:
                with open(yaurname+".txt","w+",encoding="utf-8-sig") as name:
                    name.write(titlels[0]+" , "+titlels[1])
                    name.write("\n")
                    for i in list(user_chose_output):
                        name.write(f"{i[0]}"+" , "+f"{i[1]}"+"\n")
                    messagebox.showinfo("成功","匯出成功 !")
        except:
            messagebox.showerror("錯誤","檔案名稱不合法 !")

def clear_apioutput():
    save_output.clear()
    user_chose_output.clear()


def close_function_gui():
    chose_return_default()
    chose.destroy()


def function_gui():
    global chose_tree,y_chosescrollbar,chose,chose_commbo,offoron
    if ugf.combo.get() == "":
        messagebox.showerror( "錯誤" , "請選擇API開源網站 !" )
    else:
        if offoron == 1:
            messagebox.showerror( "錯誤" , "功能視窗已開啟 !" )  
        else:
            chose = tk.Toplevel()
            chose.title( "匯出需求API" )
            chose.geometry( "500x500" )

            chose_commbo = ttk.Combobox( chose , values = ugf.sa.extraction_allapichinesetitle() )
            chose_commbo.pack()

            commbo_addframe = ttk.Frame(chose)
            commbo_addframe.pack( pady=10 )
            addframe_button1 = ttk.Button( commbo_addframe , text = "加入",command = save_user_chose )
            addframe_button1.pack( side = tk.LEFT , padx = 5 )
            addframe_button2 = ttk.Button( commbo_addframe , text = "清空" ,command = clear_user_chose )
            addframe_button2.pack( side = tk.LEFT , padx = 5 )
            addframe_button3 = ttk.Button( commbo_addframe , text = "匯出csv" , command = output_csv )
            addframe_button3.pack( side = tk.LEFT , padx = 5 )
            addframe_button4 = ttk.Button( commbo_addframe , text = "匯出txt" , command = output_txt )
            addframe_button4.pack( side = tk.LEFT , padx = 5 )
            addframe_button5 = ttk.Button( commbo_addframe , text = "關閉" , command = close_function_gui )
            addframe_button5.pack( side = tk.LEFT , padx = 5 )

            chose_tree = ttk.Treeview( chose , columns = [], show = 'headings' )
            chose_tree.pack( fill = tk.BOTH , expand = True )

            y_chosescrollbar = ttk.Scrollbar( chose , orient = "vertical" , command = chose_tree.yview )
            y_chosescrollbar.pack( side = tk.RIGHT , fill = 'y')

            offoron = 1

            chose.protocol( "WM_DELETE_WINDOW" , close_function_gui )








    


        



        






        
    
    
