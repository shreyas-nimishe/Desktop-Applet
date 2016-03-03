from Tkinter import *
from notifier import *

def get_credentials():
	root = Tk()	
	
	label1 = Label( root, text="Username")
	E1 = Entry(root, bd = 10)	

	label2 = Label( root, text="Password")
	E2 = Entry(root, bd = 10)	

	label3 = Label( root, text="E-mail")
	E3 = Entry(root, bd = 10)	

	def getDetails():
	    print type(E1.get())
	    print E2.get()
	    print E3.get()
	    print os.getcwd()
	    message('STATUS: SUCCESS', '\nUser : ' + E1.get() + ' successfully created', icon = os.path.abspath('./testing_area/img/tick_green.png'))

	submit = Button(root, text ="Create User", command = getDetails)	

	label1.pack()
	E1.pack()
	label2.pack()
	E2.pack()
	label3.pack()
	E3.pack()
	submit.pack(side = BOTTOM)

	root.mainloop()
	root.close()

def main():
	get_credentials()

if __name__ == "__main__": main()