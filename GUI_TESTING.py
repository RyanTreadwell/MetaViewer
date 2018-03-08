# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 09:12:26 2018

@author: Ryan
"""

import tkinter
from tkinter import *
from tkinter import Label
from tkinter import Frame
from tkinter import Scrollbar
from tkinter import ttk




class tableObject:
    # Container for a Recursive Table
    def __init__(self):
        self.columnQty = 0
        self.columnNames = list()
        self.columnIndexed = list()
        self.rowQty = 0
        self.rows = list()


class rowObject:
    # Container for a single rule (Row in metaTable)
    def __init__(self):
        self.colEntries = list()


class colEntry:
    # Container for a single data unit
    # (dataType string and dataValue, Value can be Table...)
    def __init__(self):
        self.dataType = "i"
        self.dataValue = 0
        self.data = [self.dataType, self.dataValue]

myTable = tableObject()

for i in range(20):
    myTable.rows.append(rowObject())
    for j in range(5):
        myTable.rows[i].colEntries.append(colEntry())


# GUI VIEW
root = Tk()

rootWindowLabel = Label(root, text="Yanman's Meta Viewer")
rootWindowLabel.pack()


listCanvasScrollbar = tkinter.Scrollbar()
listCanvas = Canvas(height=30 , width = 50, bd=3, relief=SUNKEN, yscrollcommand=listCanvasScrollbar.set)

listCanvasLabel = Label(listCanvas, text="Meta Rule list")
listCanvasLabel.pack(side=TOP)

listCanvas.pack(side=LEFT, padx=5, pady=5, fill=BOTH, expand=YES)

listCanvasScrollbar.pack(side=LEFT, fill=Y)
listCanvasScrollbar['command']=listCanvas.yview

listbox1 = Listbox(listCanvas)
for i in range(len(myTable.rows)):
   listbox1.insert(END, str(myTable.rows[i].colEntries[4].dataValue))
listbox1.pack(side=LEFT, expand=YES, fill=BOTH)


listbox2 = Listbox(listCanvas)
for i in range(len(myTable.rows)):
   listbox2.insert(END, str(myTable.rows[i].colEntries[4].dataValue))
listbox2.pack(side=LEFT, expand=YES, fill=BOTH)





detailCanvas = Canvas(height=30 , width = 50, bd=3, relief=SUNKEN)
detailCanvasLabel = Label(detailCanvas, text="Rule detail")
detailCanvasLabel.pack(side=TOP)
detailCanvas.pack(side=LEFT, padx=5, pady=5, fill=BOTH, expand=YES)


root.mainloop()