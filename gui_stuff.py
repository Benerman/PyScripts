{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "from tkinter import filedialog\n",
    "from tkinter import *"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "def browse_button():\n",
    "    # Allow user to select a directory and store it in global var\n",
    "    # called folder_path\n",
    "    global folder_path\n",
    "    filename = filedialog.askdirectory()\n",
    "    folder_path.set(filename)\n",
    "    print(filename)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "root = Tk()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "folder_path = StringVar()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "lbl1 = Label(master=root,textvariable=folder_path)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "lbl1.grid(row=0, column=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "button2 = Button(text=\"Browse\", command=browse_button)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "button2.grid(row=0, column=3, sticky=E)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "top = Toplevel()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n"
     ]
    }
   ],
   "source": [
    "root.mainloop()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "C:/Tech Inc Productions C/Davinci Resolve Database/Resolve Projects/Users/guest/Projects\n",
      "C:/Tech Inc Productions C/Davinci Resolve Database/Resolve Projects/Users/guest/Projects/TechInc Productions Ellis Wedding v3\n"
     ]
    }
   ],
   "source": [
    "from tkinter import filedialog\n",
    "from tkinter import *\n",
    "\n",
    "def source_button():\n",
    "    # Allow user to select a directory and store it in global var\n",
    "    # called folder_path\n",
    "    global source_path\n",
    "    filename = filedialog.askdirectory()\n",
    "    source_path.set(filename)\n",
    "    print(filename)\n",
    "\n",
    "def dest_button():\n",
    "    # Allow user to select a directory and store it in global var\n",
    "    # called folder_path\n",
    "    global dest_path\n",
    "    filename = filedialog.askdirectory()\n",
    "    dest_path.set(filename)\n",
    "    print(filename)\n",
    "\n",
    "root = Tk()\n",
    "root.geometry(\"400x100\")\n",
    "source_path = StringVar()\n",
    "dest_path = StringVar()\n",
    "lbl0 = Label(master=root, text=\"Choose Drive to monitor\")\n",
    "lbl0.pack(side=TOP)\n",
    "\n",
    "lbl1 = Label(master=root,textvariable=source_path)\n",
    "button1 = Button(text=\"Browse\", command=source_button)\n",
    "\n",
    "lbl1.pack(expand=True, side=LEFT)\n",
    "button1.pack(side=RIGHT)\n",
    "\n",
    "lbl3 = Label(master=root, text=\"Choose Destination for Folder Containing Files\")\n",
    "lbl3.pack(side=TOP)\n",
    "\n",
    "lbl4 = Label(master=root,textvariable=dest_path)\n",
    "button2 = Button(text=\"Browse\", command=dest_button)\n",
    "\n",
    "lbl4.pack(expand=True, side=LEFT)\n",
    "button2.pack(side=RIGHT)\n",
    "\n",
    "\n",
    "mainloop()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
