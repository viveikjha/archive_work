#!/usr/bin/env python

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, Menu
import os
window=Tk()
window.title(" A sample GUI written in PYTHON")
window.geometry('1024x768')
#window.configure(background='white')


#options that will be executed. Of course they have to be customized according to the needs. It's a sample blueprint...

def op1():
 
	lb.configure(os.system("gedit ~/Documents/box.py"))    

def op2():
 
    messagebox.showinfo('RESPONSE', ' Option no 2 executed here...')

def op3():
 
    messagebox.showinfo('RESPONSE', 'Option no 3 executed here...')

def op4():
 
    messagebox.showinfo('RESPONSE', 'Option no 4 executed here...')

def op5():
 
    messagebox.showinfo('RESPONSE', 'Option no 5 executed here...')

def op6():
 
    messagebox.showinfo('RESPONSE', 'Option no 6 executed here...')

def op7():
 
    messagebox.showinfo('RESPONSE', 'Option no 7 executed here...')

def op8():
 
    messagebox.showinfo('RESPONSE', 'Option no 8 executed here...')

def op9():
 
    messagebox.showinfo('RESPONSE', 'Option no 9 executed here...')

def op10():
 
    messagebox.showinfo('RESPONSE', 'Option no 10 executed here...')


lb=Label(window,text="Hi I'm the first GUI on this computer.",font=("Sans ",15))
lb.grid(column=0,row=1)
btn = Button(window, text="The source file..",command=op1)
btn.grid(column=1,row=1)

lb=Label(window,text="Title for option 2",font=("Sans ",15))
lb.grid(column=0,row=2)
txt = Entry(window,width=10)
txt.grid(column=1, row=2)
btn = Button(window, text="save",command=op2)
btn.grid(column=2,row=2)
btn = Button(window, text="clear",command=op2)
btn.grid(column=3,row=2)

lb=Label(window,text="Title for option 3",font=("Sans ",15))
lb.grid(column=0,row=3)
txt = Entry(window,width=10)
txt.grid(column=1, row=3)
btn = Button(window, text="save",command=op2)
btn.grid(column=2,row=3)
btn = Button(window, text="clear",command=op2)
btn.grid(column=3,row=3)

lb=Label(window,text="Title for option 4",font=("Sans ",15))
lb.grid(column=0,row=4)
txt = Entry(window,width=10)
txt.grid(column=1, row=4)
btn = Button(window, text="save",command=op2)
btn.grid(column=2,row=4)
btn = Button(window, text="clear",command=op2)
btn.grid(column=3,row=4)


lb=Label(window,text="Title for option 5",font=("Sans ",15))
lb.grid(column=0,row=5)
txt = Entry(window,width=10)
txt.grid(column=1, row=5)
btn = Button(window, text="save",command=op2)
btn.grid(column=2,row=5)
btn = Button(window, text="clear",command=op2)
btn.grid(column=3,row=5)

lb=Label(window,text="Title for option 6",font=("Sans ",15))
lb.grid(column=0,row=6)
txt = Entry(window,width=10)
txt.grid(column=1, row=6)
btn = Button(window, text="save",command=op2)
btn.grid(column=2,row=6)
btn = Button(window, text="clear",command=op2)
btn.grid(column=3,row=6)

lb=Label(window,text="Title for option 7",font=("Sans ",15))
lb.grid(column=0,row=7)
txt = Entry(window,width=10)
txt.grid(column=1, row=7)
btn = Button(window, text="save",command=op2)
btn.grid(column=2,row=7)
btn = Button(window, text="clear",command=op2)
btn.grid(column=3,row=7)

lb=Label(window,text="Title for option 8",font=("Sans ",15))
lb.grid(column=0,row=8)
txt = Entry(window,width=10)
txt.grid(column=1, row=8)
btn = Button(window, text="save",command=op2)
btn.grid(column=2,row=8)
btn = Button(window, text="clear",command=op2)
btn.grid(column=3,row=8)

lb=Label(window,text="Title for option 9",font=("Sans ",15))
lb.grid(column=0,row=9)
txt = Entry(window,width=10)
txt.grid(column=1, row=9)
btn = Button(window, text="save",command=op2)
btn.grid(column=2,row=9)
btn = Button(window, text="clear",command=op2)
btn.grid(column=3,row=9)

lb=Label(window,text="Title for option 10",font=("Sans ",15))
lb.grid(column=0,row=10)
txt = Entry(window,width=10)
txt.grid(column=1, row=10)
btn = Button(window, text="save",command=op2)
btn.grid(column=2,row=10)
btn = Button(window, text="clear",command=op2)
btn.grid(column=3,row=10)



lb=Label(window,text=" A sample options menu :",font=("Sans",15))
lb.grid(column=5,row=13)


chk_state = BooleanVar()
 
chk_state.set(False) #set check state
 

def response():
	lb.configure(text='Thanks for your review!')
	chk.grid(column=0, row=20)



combo = Combobox(window)
 
combo['values']= ("option1", "option 2", "option 3","option  4", "option 5", "Text")
 
combo.current(1) #set the selected item
 
combo.grid(column=5, row=15)

chk = Checkbutton(window, text=' Sample checkbox (if required)', var=chk_state,command=response) 
chk.grid(column=0, row=16)
'''
rad1 = Radiobutton(window,text='First', value=1)
 
rad2 = Radiobutton(window,text='Second', value=2)
 
rad3 = Radiobutton(window,text='Third', value=3)
 
rad1.grid(column=0, row=14)
 
rad2.grid(column=1, row=14)
 
rad3.grid(column=2, row=14)

'''

lb=Label(window,text="Written by Vivek Jha at ARIES Nainital",
		 font = "Helvetica 16 bold italic")
lb.grid(column=5,row=38)

menu = Menu(window)
new_item = Menu(menu)
new_item.add_command(label='New')
menu.add_cascade(label='File', menu=new_item)
menu.add_cascade(label='Edit', menu=new_item)
menu.add_cascade(label='View', menu=new_item)
menu.add_cascade(label='Format', menu=new_item)
menu.add_cascade(label='Tools', menu=new_item)
menu.add_cascade(label='About', menu=new_item)
window.config(menu=menu)

btn = Button(window, text="Save",command=op2)
btn.grid(column=0,row=25)
btn = Button(window, text="Cancel",command=op2)
btn.grid(column=1,row=25)
btn = Button(window, text="Clear all",command=op2)
btn.grid(column=2,row=25)
btn = Button(window, text="exit",command=op2)
btn.grid(column=3,row=25)



window.mainloop()


		 

