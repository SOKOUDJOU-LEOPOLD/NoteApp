# Author: SGL Company
# Purpose: To remind you of your priorities.
# Name: Notes App

# The Treeview widget is found in tkinter.ttk

from tkinter import *
from tkinter import ttk
import tkinter as tk
import sqlite3
import pyttsx3
import time



class Window(Tk):

    def __init__(self): # Constructor
        super(Window, self).__init__()
        #The super() function is used to give access to methods and properties
        # of a parent or sibling class. The super() function returns an object
        # that represents the parent class. For Inheritance.
        self.config(background="lightpink")
        self.title("Notes App")
        self.minsize(150,200)
        # win.wm_iconbitmap("myicon.png")
        self.createLabel()
        self.createLayout()
        self.createTextBox()
        self.createTreeView()
        self.database()
        self.loadTasks()
        self.count = 0


    def change_label(self): ###################################
        self.label.configure(text=self.task.get())

    def createLabel(self):
        labelFont = ("times",15,"italic","bold")
        self.label = Label(self, text = "Task:")
        self.label.config(font=labelFont)
        self.label.grid(column=0,row=0)

    def createLayout(self):
        buttonFont = ("times",15,"italic","bold")
        self.button1 = Button(self, text="Add Task", width=20, background="blue", command=self.addTask)
        self.button2 = Button(self, text="Delete Task", width=20, background="red",command=self.deleteTask)
        self.button3 = Button(self, text="Load Tasks", width=20, background="yellow",command=self.loadTasks)
        self.button4 = Button(self, text="Hear Tasks", width=20, background="violet",command=self.hearTasks)
        self.button1.config(font=buttonFont)
        self.button2.config(font=buttonFont)
        self.button3.config(font=buttonFont)
        self.button4.config(font=buttonFont)
        self.button1.grid(column=0, row=2, pady=5, padx=10)
        self.button2.grid(column=0, row=3, pady=5, padx=10)
        self.button3.grid(column=0, row=4, pady=5, padx=10)
        self.button4.grid(column=0, row=5, pady=10, padx=10)

    def createTextBox(self):
        self.task=StringVar()
        self.entry=Entry(self, width=37, textvariable = self.task) #You can also use Text.
        self.entry.focus()
        self.entry.grid(column=0,row=1, pady=5,padx=0)

    def createTreeView(self):
        self.myTree=ttk.Treeview(self)
        #Define our columns
        self.myTree["columns"]=("ID","TASKS")
        #Format our columns
        self.myTree.column("#0", width=10, minwidth=15)
        self.myTree.column("ID", width=40, anchor =E)
        self.myTree.column("TASKS", width=250, anchor=W)
        self.myTree.grid(column=0,row=6,pady=10, padx=20)
        # Create Headings
        self.myTree.heading("#0", text= " ", anchor=CENTER)
        self.myTree.heading("ID",text= "ID", anchor=CENTER)
        self.myTree.heading("TASKS",text= "TASKS", anchor=CENTER)

    def database(self):
        self.conn = sqlite3.connect('Notes.sqlite')
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS Notes (id INTEGER, tasks TEXT)')
        self.conn.commit()
        self.cur.close()

    def addTask(self):
        ##################################
        self.conn = sqlite3.connect('Notes.sqlite')
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS Notes (id INTEGER, tasks TEXT)')
        ##################################
        self.count+=1
        self.myTree.insert('', tk.END, values=(self.count, self.task.get()))
        self.cur.execute("INSERT INTO Notes(id,tasks) VALUES(?,?)", (self.count, self.task.get()))
        self.filehandler = open("notes.txt", "a")
        self.filehandler.write(self.task.get()+"\n")
        self.filehandler.close()
        #################################
        self.conn.commit()
        self.cur.close()

    def deleteTask(self):
        #################################
        self.conn = sqlite3.connect('Notes.sqlite')
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS Notes (id INTEGER, tasks TEXT)')
        #self.conn.commit()
        #self.cur.close()
        ###################################
        self.x=self.myTree.selection()[0]
        #print(x)
        self.dictTask=self.myTree.item(self.x)
        #print(dictTask)
        self.currentTask=self.dictTask["values"][1]
        #print(currentTask)
        self.currentId= self.dictTask["values"][0]
        #print(currentId)
        self.myTree.delete(self.x)
        #print(self.myTree.get_children())
        #for item in self.myTree.get_children():
         #   self.myTree.delete(item)
        self.cur.execute("DELETE FROM Notes WHERE id=?", (self.currentId,))
        filehandler = open("notes.txt", "r")
        self.lines = filehandler.readlines()
        filehandler.close()
        counting=-1
        print(self.lines)
        print(self.currentTask)
        if self.currentTask+"\n" in self.lines:
            print(True)
            self.lines.remove(self.currentTask+"\n")
        print(self.lines)
        filehandler.close() ###############################
        filehandler = open("notes.txt", "w")

        for line in self.lines:
            filehandler.write(line)
        filehandler.close()
        ###########################
        self.conn.commit()
        self.cur.close()

    #
    def loadTasks(self):
        ######################################
        self.conn = sqlite3.connect('Notes.sqlite')
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS Notes (id INTEGER, tasks TEXT)')
        #self.commit()
        #self.cur.close()
        #######################################
        for item in self.myTree.get_children():
            self.myTree.delete(item)

        self.cur.execute("SELECT * FROM Notes")
        self.rows = self.cur.fetchall()
        totalrows = len(self.rows)
        for i in self.rows:
            self.myTree.insert("", 'end', values=i)

        # say the number of tasks
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[1].id)
        self.engine.setProperty("rate", 170)
        self.engine.say("There are " + str(totalrows) + " number of tasks.")
        self.engine.runAndWait()
        #################
        self.conn.commit()
        self.cur.close()

    #
    def hearTasks(self):
        #self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", self.voices[1].id)
        self.engine.setProperty("rate", 170)
        self.filehandler = open("notes.txt", "r")
        self.lines = self.filehandler.readlines()
        self.filehandler.close()
        self.n = 0
        for line in self.lines:
            self.n += 1
            self.engine.say(line)
            time.sleep(0.25)
            self.engine.runAndWait()















window = Window()
window.mainloop()