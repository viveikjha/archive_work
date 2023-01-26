from tkinter import *
from tkinter import ttk,filedialog,messagebox
from astropy.io import fits
import os,sys
from glob import glob



class header_edit:
    def __init__(self,master):
        self.fil=glob("*fits")
        master.geometry("800x600")

        self.lb1=Label(master,text=" ##A basic GUI for Header editing procedure## ")
        self.lb1.place(x=200,y=20)

        self.see=Button(master, text='See header',command=self.see_header)
        self.see.place(x=100,y=50)


        self.b1=Button(master, text='APPEND',command=self.add_header)
        self.b1.place(x=450,y=200)
        
        self.b1=Button(master, text='REMOVE',command=self.delete_header)
        self.b1.place(x=450,y=300)

        self.lb1=Label(master,text=" Modify Header data: ")
        self.lb1.place(x=10,y=100)


        self.lb1=Label(master,text=" Add new Header: ")
        self.lb1.place(x=10,y=200)


        self.lb1=Label(master,text=" Remove Header: ")
        self.lb1.place(x=10,y=300)


        self.lb1=Label(master,text=" Change Header name:")
        self.lb1.place(x=10,y=400)

        self.lb1=Label(master,text=" Add comment: ")
        self.lb1.place(x=10,y=500)
        
    
        self.var1 = IntVar()
        self.cb1=Checkbutton(master, text="Yes", variable=self.var1)
        self.cb1.place(x=600,y=200)
        self.var2 = IntVar()
        self.cb2=Checkbutton(master, text="No", variable=self.var2)
        self.cb2.place(x=660,y=200)
        master.bind("<Return>", (lambda event: self.var_states1()))
  
  

 
 
    def var_states1(self):
        self.c=self.var1.get()
       
        if (self.c==1):
            self.textbox()
        else:
            self.elfg=Label(text=" You did not want to enter right?")
            self.elfg.place(x=400,y=240) 

 
    def input_val(self):
        self.inputval=self.textBox.get("1.0","end-1c")
        print(self.inputval)
   
    def see_header(self):
         self.b=fits.getheader(self.fil[11],0)
         self.data=fits.getdata(self.fil[11])
         messagebox.showinfo('HEADER INFO',self.b)
         #print(self.inputval)
    
    def textbox(self):
        self.textBox=Text(height=2,width=20)
        self.textBox.place(x=200,y=200)
        self.buttonc=Button(text="Enter",command=lambda:self.input_val())
        self.buttonc.place(x=350,y=200)
        self.lb=Label(text="Kindly add the new header keyword")
        self.lb.place(x=400,y=140)
        self.bind("<Return>", (lambda event: self.input_val()))
  
  
  
    def add_header(self):
        s=self.inputval
        self.b.insert('NAXIS1', ("%s"%s,"second append from here..."))
        fits.writeto(self.fil[11], self.data,self.b,overwrite=True)
        print("Header appendeded succesfully!!!!")
    
    def delete_header(self):
        s=self.inputval
        self.b.remove('%s'%s)
        fits.writeto(self.fil[11], self.data,self.b,overwrite=True)
        print("header removed succesfully!!!!")
    
    
    
    
root=Tk()
all=header_edit(root)
root.title("GUI for FITS header editing")
root.pack_propagate(0)
root.mainloop()

 
