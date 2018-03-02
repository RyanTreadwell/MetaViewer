# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 20:26 2018

@author: Ryan
"""
##IMPORTS
import tkinter
from tkinter import *
from tkinter import ttk




##Container for a single data unit (dataType string and dataValue, Value can be Table...)
class colEntry:
   def __init__(self):
      self.dataType = 'i';
      self.dataValue = 0;
      self.data = [self.dataType,self.dataValue]

##Container for a single rule (Row in metaTable)
class rowObject:
    def __init__(self):
      self.colEntries = list();

##Container for a single NAV Route (Row in metaTable)
class navObject:
    def __init__(self,blobLength):
      self.blobLength = blobLength;
      self.listData = list();
      self.lineCount = 0;
      self.routeName = '';
         
##Container for a Recursive Table
class tableObject:
   def __init__(self):
      self.columnQty = 0;
      self.columnNames = list();
      self.columnIndexed = list();
      self.rowQty = 0;
      self.rows = list();
      
##Table Parsing Function, outputs tableObject
#Function which takes in the raw meta data and parses into a table.
#Recursively calls itself to build sub-tables.

def buildTable(currentPos, ruleData):
   tick = 0; # offset counter.
   #print(['Start of Table: ', currentPos,tick])
   newTable = tableObject(); # init table object.
   newTable.columnQty = int(ruleData[currentPos])
   tick = tick+1;
   #print(['Column Qty: ',currentPos,tick,newTable.columnQty])
   for i in range(newTable.columnQty):
      newTable.columnNames.append(ruleData[currentPos + tick]);
      newTable.columnIndexed.append(ruleData[currentPos + newTable.columnQty + tick]);
      tick = tick + 1;
   #print(['Column Names/IDX: ',currentPos,tick,newTable.columnNames[:],newTable.columnIndexed[:]])
   newTable.rowQty = int(ruleData[currentPos + 2 * newTable.columnQty + 1]);
   #print(['Row Qty: ',currentPos,tick,newTable.rowQty])
   tick = 2 * newTable.columnQty + 2;
   if newTable.columnQty == 0:
      tick = tick + 1;
   for i in range(newTable.rowQty):
      newTable.rows.append(rowObject());
      for j in range(newTable.columnQty):
         newTable.rows[i].colEntries.append(colEntry());
         for k in range(2):
            if k == 0:
               callTable = 0;
               callNav = 0;
               #print([currentPos,tick,currentPos + tick])
               newTable.rows[i].colEntries[j].dataType = ruleData[currentPos + tick];
               #print([i,j,k,currentPos,tick,newTable.rows[i].colEntries[j].dataType])
               if (ruleData[currentPos + tick] == 'TABLE'):
                  callTable = 1;
               if (ruleData[currentPos + tick] == 'ba'):
                  callNav = 1;
               tick = tick+1;
            elif k == 1:
               if (callTable == 1):
                  #print('SUBTABLE')
                  [newTable.rows[i].colEntries[j].dataValue, currentPos] = buildTable(currentPos + tick,ruleData);
                  tick = 0;
                  #print('RETURN')
               elif (callNav == 1):
                  [newTable.rows[i].colEntries[j].dataValue, currentPos] = buildNav(currentPos + tick,ruleData);
                  tick = 0;
               else:
                  newTable.rows[i].colEntries[j].dataValue = ruleData[currentPos + tick];
                  #print([i,j,k,currentPos,tick,newTable.rows[i].colEntries[j].dataValue])
                  tick = tick + 1;
            newTable.rows[i].colEntries[j].data = [newTable.rows[i].colEntries[j].dataType, newTable.rows[i].colEntries[j].dataValue]
   #print([currentPos,tick])
   return (newTable, currentPos + tick)


## Creates a navObject from the rule data to store as a dataValue in a colEntry
def buildNav(currentPos, ruleData):
   tick = 0;
   newNav = navObject(int(ruleData[currentPos]));
   newNav.lineCount = 0;
   navAsciiLength = 0;
   tick = tick + 1
   newNav.routeName = ruleData[currentPos + tick]
   newNav.lineCount = newNav.lineCount + 1;
   navAsciiLength = navAsciiLength + len(newNav.routeName) + 2;
   tick = tick + 1
   while navAsciiLength < newNav.blobLength:
      newNav.listData.append(ruleData[currentPos + tick]);
      newNav.lineCount = newNav.lineCount + 1;
      navAsciiLength = navAsciiLength + len(ruleData[currentPos + tick]) + 2;
      tick = tick + 1;
   return (newNav, currentPos + tick)

def tableReader(metaTable,outFile,spcqty):
   spc = ''
   for i in range(spcqty):
      spc = '  ' + spc
   outFile.write(str(metaTable.columnQty) + '\n')
   #print(spc + 'COLQTY = ' + str(metaTable.columnQty))
   for i in range(metaTable.columnQty):
      outFile.write(metaTable.columnNames[i] + '\n')
      #print(spc + 'COL_' + str(i) + '_NAME = '+  metaTable.columnNames[i])
   for i in range(metaTable.columnQty):
      outFile.write(metaTable.columnIndexed[i] + '\n')
      #print(spc + 'IDX_' + str(i) + '_IDX = ' + metaTable.columnIndexed[i])
   outFile.write(str(metaTable.rowQty) + '\n')
   #print(spc + 'ROWQTY = ' + str(metaTable.rowQty))
   for i in range(metaTable.rowQty):
      #print(spc + 'ROW# : ' + str(i) + '===========================================')
      for j in range(metaTable.columnQty):
         #print(spc + str([i,j])+ '---------------------------------------------')
         #print(spc + 'COL : ' + metaTable.columnNames[j])
         outFile.write(metaTable.rows[i].colEntries[j].dataType + '\n')
         #print(spc + 'DTYPE = ' + metaTable.rows[i].colEntries[j].dataType)
         if (metaTable.rows[i].colEntries[j].dataType == 'TABLE'):
            spcqty = spcqty + 1;
            tableReader(metaTable.rows[i].colEntries[j].dataValue,outFile,spcqty)
            spcqty = spcqty - 1;
         elif (metaTable.rows[i].colEntries[j].dataType == 'ba'):
            spcqty = spcqty + 1;
            outFile.write(str(metaTable.rows[i].colEntries[j].dataValue.blobLength) + '\n')
            #print(spc + '*NAVBLOBLEN*' + '   ' + str(metaTable.rows[i].colEntries[j].dataValue.blobLength))
            outFile.write(str(metaTable.rows[i].colEntries[j].dataValue.routeName) + '\n')
            #print(spc + '*NAVNAME*' + '   ' + str(metaTable.rows[i].colEntries[j].dataValue.routeName))
            for k in range(metaTable.rows[i].colEntries[j].dataValue.lineCount -1):
               outFile.write(str(metaTable.rows[i].colEntries[j].dataValue.listData[k]) + '\n')
               #print(spc + '*NAV*' + '  ' + str(metaTable.rows[i].colEntries[j].dataValue.listData[k]))
            spcqty = spcqty - 1;
         else:
            outFile.write(str(metaTable.rows[i].colEntries[j].dataValue) + '\n')
            #print(spc + 'DVAL = ' + str(metaTable.rows[i].colEntries[j].dataValue))

def tableStringifier(tableObject):
   stringList = list();
   for i in range(len(tableObject.rows)):
      for j in range(len(tableObject.rows[i].colEntries)):
         entryList = list();
         entryList.append(tableObject.rows[i].colEntries[j].dataType)
         if (tableObject.rows[i].colEntries[j].dataType == 'TABLE'):
            entryList.append(tableStringifier(tableObject.rows[i].colEntries[j].dataValue))
         elif (tableObject.rows[i].colEntries[j].dataType == 'ba'):
            entryList.append(navStringifier(tableObject.rows[i].colEntries[j].dataValue))
         else:
            entryList.append(tableObject.rows[i].colEntries[j].dataValue)
         stringList.append(entryList[:])
   return(stringList)

def navStringifier(navObject):
   stringList = list();
   stringList.append(navObject.blobLength);
   stringList.append(navObject.routeName);
   for i in range(len(navObject.listData)):
      stringList.append(navObject.listData[i])
   return(stringList)



##Create File Object and open file
inputFileObject = open('Yanman Gambling Meta.met', 'r');
##Read File Object to string
fileText = inputFileObject.read();
##Close File Object
inputFileObject.close();
##Split String on newlines
fileLines = fileText.splitlines();
##Grab Static Header Data
tableQty = fileLines[0];#Should Always be 1
tableName = fileLines[1];#Should Always be CondAct 
tableColumnQty = fileLines[2];#Should Always be 5
ruleQty = fileLines[13];#Changes, 0 to inf.
ruleData = fileLines[2:];#Changes, at least 10x ruleQty in line count.`

[myTable,lineQty] = buildTable(0,ruleData);

outputFileObject = open('outFile.met', 'w+')

outputFileObject.write(tableQty + '\n')
outputFileObject.write(tableName + '\n')
tableReader(myTable,outputFileObject,0);
outputFileObject.close();


listOfStates = list();
countOfStateRules = list();
for row in myTable.rows[:]:
   if row.colEntries[4].dataValue in listOfStates:
      countOfStateRules[listOfStates.index(row.colEntries[4].dataValue)] = countOfStateRules[listOfStates.index(row.colEntries[4].dataValue)] + 1
   else:
      listOfStates.append(row.colEntries[4].dataValue)
      countOfStateRules.append(1)
      
for stateNum in range(len(listOfStates)):
   print('STATE NAME = ' + str(listOfStates[stateNum]) + ', RULE QTY = ' + str(countOfStateRules[stateNum]))
   stateRuleNo = 1;
   for ruleNum in range(len(myTable.rows)):
      if myTable.rows[ruleNum].colEntries[4].dataValue == listOfStates[stateNum]:
         print('  ' + 'RULE # ' + str(stateRuleNo))
         stateRuleNo = stateRuleNo + 1;
         ezROW = list();
         for colNum in range(len(myTable.rows[ruleNum].colEntries)):
            ezCOL = list();
            ezCOL.append(str(myTable.rows[ruleNum].colEntries[colNum].dataType))
            if myTable.rows[ruleNum].colEntries[colNum].dataType == 'TABLE':
               ezCOL.append(tableStringifier(myTable.rows[ruleNum].colEntries[colNum].dataValue))
            elif myTable.rows[ruleNum].colEntries[colNum].dataType == 'ba':
               ezCOL.append(navStringifier(myTable.rows[ruleNum].colEntries[colNum].dataValue))
            else:
               ezCOL.append(str(myTable.rows[ruleNum].colEntries[colNum].dataValue))
            ezROW.append(ezCOL);
         print('  ' + str(ezROW))
   
   
## GUI VIEW
master = tkinter.Tk()

scrollbar = Scrollbar(master)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(master, yscrollcommand=scrollbar.set)
for i in range(len(myTable.rows)):
   for j in range(len(myTable.rows[i].colEntries)):
      listbox.insert(END, Button(master, text=str(myTable.rows[i].colEntries[j].dataValue))
      listbox.pack()
      
scrollbar.config(command=listbox.yview)
master.mainloop()




