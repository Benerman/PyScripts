# from tkinter import *

# def browse_button():
#     # Allow user to select a directory and store it in global var
#     # called folder_path
#     global folder_path
#     filename = filedialog.askdirectory()
#     folder_path.set(filename)
#     print(filename)


# root = Tk()
# root.geometry("500x100") #Width x Height
# folder_path = StringVar()
# lbl1 = Label(master=root,textvariable=folder_path)
# lbl1.grid(row=0, column=1)
# button2 = Button(text="Browse", command=browse_button)
# button2.grid(row=0, column=3, sticky=E)

# mainloop()

from tkinter import filedialog
from tkinter import *

def source_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global source_path
    filename = filedialog.askdirectory()
    source_path.set(filename)
    print(filename)

def dest_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global dest_path
    filename = filedialog.askdirectory()
    if len(filename) > 48:
    	short_filename = f'{filename[:21]}...{filename[:-20]}'
    	dest_path.set(short_filename)
    	print(short_filename)
    else:
    	dest_path.set(filename[:48])
    	print(filename)

root = Tk()
root.geometry("400x100")
source_path = StringVar()
dest_path = StringVar()
lbl0 = Label(master=root, text="Choose Drive to monitor")
lbl0.grid(row=0, column=1)

lbl1 = Label(master=root,text="Source: ")
lbl2 = Label(master=root,textvariable=source_path)
button1 = Button(text="Browse", command=source_button)

lbl1.grid(row=1, column=0)
lbl2.grid(row=1, column=1)
button1.grid(row=1, column=2)

lbl3 = Label(master=root, text="Choose Destination for Folder Containing Files")
lbl3.grid(row=2, column=1)

lbl4 = Label(master=root,text="Destination: ")
lbl5 = Label(master=root,textvariable=dest_path)
button2 = Button(text="Browse", command=dest_button)

lbl4.grid(row=3, column=0)
lbl5.grid(row=3, column=1)
button2.grid(row=3, column=2)


mainloop()