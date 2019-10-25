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
   "execution_count": 77,
   "metadata": {},
   "outputs": [
    {
     "ename": "TclError",
     "evalue": "cannot use geometry manager pack inside . which already has slaves managed by grid",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mTclError\u001b[0m                                  Traceback (most recent call last)",
      "\u001b[1;32m<ipython-input-77-3a60b68b5845>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[0;32m     28\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     29\u001b[0m \u001b[0mlbl1\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mpack\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mfill\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mX\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mexpand\u001b[0m\u001b[1;33m=\u001b[0m\u001b[1;32mTrue\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mside\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mLEFT\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m---> 30\u001b[1;33m \u001b[0mbutton1\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mpack\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mfill\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mX\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mside\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mLEFT\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m     31\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     32\u001b[0m \u001b[0mlbl3\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mLabel\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mmaster\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mroot\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mtext\u001b[0m\u001b[1;33m=\u001b[0m\u001b[1;34m\"Choose Destination for Folder Containing Files\"\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32mC:\\ProgramData\\Anaconda3\\lib\\tkinter\\__init__.py\u001b[0m in \u001b[0;36mpack_configure\u001b[1;34m(self, cnf, **kw)\u001b[0m\n\u001b[0;32m   2141\u001b[0m         self.tk.call(\n\u001b[0;32m   2142\u001b[0m               \u001b[1;33m(\u001b[0m\u001b[1;34m'pack'\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;34m'configure'\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_w\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m-> 2143\u001b[1;33m               + self._options(cnf, kw))\n\u001b[0m\u001b[0;32m   2144\u001b[0m     \u001b[0mpack\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mconfigure\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mconfig\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mpack_configure\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m   2145\u001b[0m     \u001b[1;32mdef\u001b[0m \u001b[0mpack_forget\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;31mTclError\u001b[0m: cannot use geometry manager pack inside . which already has slaves managed by grid"
     ]
    }
   ],
   "source": [
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
    "\n",
    "source_path = StringVar()\n",
    "dest_path = StringVar()\n",
    "lbl0 = Label(master=root, text=\"Choose Drive to monitor\")\n",
    "lbl0.pack(side=TOP)\n",
    "\n",
    "lbl1 = Label(master=root,textvariable=source_path)\n",
    "button1 = Button(text=\"Browse\", command=source_button)\n",
    "\n",
    "lbl1.pack(fill=X, expand=True, side=LEFT)\n",
    "button1.pack(fill=X, side=LEFT)\n",
    "\n",
    "lbl3 = Label(master=root, text=\"Choose Destination for Folder Containing Files\")\n",
    "lbl3.pack(side=TOP)\n",
    "\n",
    "lbl4 = Label(master=root,textvariable=dest_path)\n",
    "button2 = Button(text=\"Browse\", command=dest_button)\n",
    "\n",
    "lbl4.pack(fill=X, expand=True, side=LEFT)\n",
    "button2.pack(side=LEFT)\n",
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
