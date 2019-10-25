from tkinter import *

class SDGui(object):
	def __init__(self, master):
		self.master = master
		master.title("SD Card Watcher")

		self.label = Label(master, text="Select SD Card Drive to Monitor")
		self.label.pack()

		self.greet_button = Button(master, text="Greet", command=self.greet)
		self.greet_button.pack(side=LEFT)

		self.close_button = Button(master, text="Exit", command=master.quit)
		self.close_button.pack()

	def greet(self):
		print("Greetings!")

def main():
	from tkinter import Tk, Label, Button, LEFT, RIGHT
	root = Tk()
	gui = SDGui(root)
	root.mainloop()


if __name__ == '__main__':
	main()
