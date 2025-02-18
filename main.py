import zipfile
import os
import tkinter as tk
from tkinter import  filedialog
archive_list =[]

app = tk.Tk()
app.geometry("500x500")
app.title("Uarchiver")
icon = tk.PhotoImage(file="zip.png")
app.iconphoto(True,icon)
files_ = []
folder_selected = None
filame = tk.StringVar()
def opendir():
    listbox.delete(0, tk.END)
    global folder_selected
    folder_selected = filedialog.askdirectory(title= "Select a folder for compression")
    if folder_selected:
        label.config(text=f"{folder_selected} is selected")
    try:
            for var in os.listdir(folder_selected):
                listbox.insert(tk.END,var)
    except TypeError:
        pass
    except FileNotFoundError:
        pass
def openfile():
    global files_
    global folder_selected
    folder_selected = filedialog.askopenfilename(title= "Select a file for compression")
    files_.append(folder_selected)
    if folder_selected:
        label.config(text=f"{os.path.basename(folder_selected)} is selected")
    listbox.insert(tk.END,folder_selected)
def create_compressor():
    try:
        if os.path.isdir(folder_selected):
            if filame.get():
                filename = filame.get()
            else:
                filename = os.path.basename(folder_selected)

            with zipfile.ZipFile(filename+".zip","w",zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(folder_selected):
                    for file in files:
                        file_path = os.path.join(root,file)
                        arcname = os.path.relpath(file_path,folder_selected)
                        zipf.write(file_path,arcname)
        elif os.path.isfile(folder_selected):
            if filame.get():
                s = filame.get()
            else:
                s = "archive.zip"
            with zipfile.ZipFile(s+".zip","w") as zipf:
                for file in files_:
                    if filname.get():
                        zipf.write(file,arcname=f"/{filname.get()}/"+os.path.basename(file))
                    else:
                        zipf.write(file,arcame=f"/archive/"+os.path.basename(file))
    except TypeError:
        pass
filepath = ""
def decompressor():
    global filepath
    listbox.delete(0,tk.END)
    filepath = filedialog.askopenfilename(filetypes=(("Zip Files","*.zip"),("All Files","*.*")))
    with zipfile.ZipFile(filepath,"r") as zipf:
        filelist = zipf.namelist()
        for f in filelist:
            listbox.insert(tk.END,f)

def decompress():
    if filepath.endswith(".zip"):
        with zipfile.ZipFile(filepath,"r") as zipf:
            zipf.extractall(filepath.removesuffix(".zip"))
menu_bar= tk.Menu(app)
folder_menu = tk.Menu(menu_bar,tearoff=0)
folder_menu.add_command(label = "Compress Folder", command=opendir)
folder_menu.add_command(label = "Compress File", command=openfile)
folder_menu.add_command(label = "Decompress",command= decompressor)
menu_bar.add_cascade(label="File", menu=folder_menu)

btn = tk.Button(app,text="compress", height= 2, width= 5,background="pink",command=create_compressor)
btn.place(x=50,y=200)
btn2 = tk.Button(app,text="decompress", height= 2, width= 9,background="pink",command=decompress)
btn2.place(x=150,y=200)
label = tk.Label(app, text="No Folder Selected", font=("Cambria", 12))
label.place(x=0, y=0)
listbox = tk.Listbox(app,height=10,width=30)
listbox.place(x=20,y=20)
filname= tk.Entry(textvariable=filame,width=15).place(x=0,y=240)
app.config(menu=menu_bar)
app.mainloop()