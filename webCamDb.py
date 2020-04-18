#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from PIL import ImageTk
import PIL.Image
from tkinter.ttk import * 


# # Databse Connectivity

# In[2]:


import mysql.connector
db_connection = mysql.connector.connect(
host= "localhost",
user= "root",
passwd= "root")
print(db_connection)


# In[3]:


db_cursor = db_connection.cursor(buffered=True)

db_cursor.execute("DROP DATABASE my_first_db")
db_cursor.execute("CREATE DATABASE my_first_db")
db_cursor.execute("SHOW DATABASES")
db_cursor.execute("USE my_first_db")
db_cursor.execute("CREATE TABLE WebCamDB (Id VARCHAR(255) PRIMARY KEY,Location VARCHAR(255))")

# student_sql_query = "INSERT INTO WebCamDB(Id,Location) VALUES(01, 'John')"


# # GUI for WEBCAMERA

# In[4]:


from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def show_database():
    db_cursor.execute("Select * from WebCamDB")
    canvas=Tk()
    canvas.title('WebCam DB')
    label = tk.Label(canvas, text="WebCamera Database", font=("Arial",20)).grid(row=0, columnspan=3)
    
    cols = ('Camera Serial No.', 'Location')
    listBox = ttk.Treeview(canvas, columns=cols, show='headings')
    for col in cols:
        listBox.heading(col, text=col)    
    listBox.grid(row=1, column=0, columnspan=2)
    tempList=[]
    for db in db_cursor:
        tempList.append(db)
    for (name, score) in enumerate(tempList, start=1):
        listBox.insert("", "end", values=(score))
    closeButton = tk.Button(canvas, text="Close", width=15, command=exit).grid(row=4, column=1)

#     canvas.geometry('250x100')
    canvas.configure(bg='white')
#     message=tk.Label(canvas, text=db_cursor,fg='green',bg='white',font=("arial", 10,'bold'))
#     message.place(x=10,y=50)
#     canvas.after(1000, lambda: canvas.destroy())
    canvas.mainloop()
    
def show_entry_fields():
    var1=str(srno_entry.get())
    var2=str(location_entry.get())
    sql_query = "INSERT INTO WebCamDB(Id,Location) VALUES("+var1+", '"+var2+"')"
    db_cursor.execute(sql_query)
    canvas=Tk()
    canvas.title('Successfully added')
    canvas.geometry('250x100')
    canvas.configure(bg='white')
    message=tk.Label(canvas, text="Camera Details Added Successfully!",fg='green',bg='white',font=("arial", 10,'bold'))
    message.place(x=10,y=50)
    canvas.after(1000, lambda: canvas.destroy())
    canvas.mainloop()
    
    
window=Tk()
window.title('WebCamInterface') 
window.geometry('750x500+10+10') 
window.configure(background = 'black')
# print(img)

lbl=Label(window, text="WEB CAMERA DETAILS", fg='white',bg='black', font=("Algerian", 20,'bold'))
lbl.place(x=225, y=125)

srno=tk.Label(window, text="Camera Serial No.",fg='white',bg='black', font=("Algerian", 15))
srno.place(x=125,y=200)
srno_entry = tk.Entry(window,font=("Comic Sans", 15))
srno_entry.place(x=325,y=200)

location=tk.Label(window, text="Camera Location",fg='white',bg='black',font=("Algerian", 15))
location.place(x=125,y=250)
location_entry = tk.Entry(window,font=("Comic Sans", 15))
location_entry.place(x=325,y=250)

add=tk.Button(window,text='ADD', command=show_entry_fields,font=("Comic Sans", 14))
add.place(x=350,y=300)
show=tk.Button(window,text='Show Database', command=show_database,font=("Comic Sans", 14))
show.place(x=600,y=350)

images=[]
for i in range(0,5):
    temp=i+1
    path="images/image"+str(temp)+".jpg"
    im = PIL.Image.open(path)
    im=im.resize((150,100))
    images.append(ImageTk.PhotoImage(im,master=window))

image1= Label(window, image=images[0])
image1.place(x=0,y=0)
image2= Label(window, image=images[1])
image2.place(x=150*1,y=0)
image3= Label(window, image=images[2])
image3.place(x=150*2,y=0)
image4= Label(window, image=images[3])
image4.place(x=150*3,y=0)
image5= Label(window, image=images[4])
image5.place(x=150*4,y=0)

down=400

dimage1= Label(window, image=images[0])
dimage1.place(x=0,y=down)
dimage2= Label(window, image=images[1])
dimage2.place(x=150*1,y=down)
dimage3= Label(window, image=images[2])
dimage3.place(x=150*2,y=down)
dimage4= Label(window, image=images[3])
dimage4.place(x=150*3,y=down)
dimage5= Label(window, image=images[4])
dimage5.place(x=150*4,y=down)


window.mainloop()


# In[5]:


db_cursor.execute("Select * FROM WebCamDB")
dataset=[]
for db in db_cursor:
    dataset.append(db)
dataset=pd.DataFrame(dataset)
dataset


# In[ ]:





# In[ ]:




