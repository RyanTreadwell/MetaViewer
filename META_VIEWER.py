# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 20:26 2018

@author: Ryan
"""
##IMPORTS
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
               #print([currentPos,tick,currentPos + tick])
               newTable.rows[i].colEntries[j].dataType = ruleData[currentPos + tick];
               #print([i,j,k,currentPos,tick,newTable.rows[i].colEntries[j].dataType])
               if (ruleData[currentPos + tick] == 'TABLE'):
                  callTable = 1;
               tick = tick+1;
            elif k == 1:
               if (callTable == 1):
                  #print('SUBTABLE')
                  [newTable.rows[i].colEntries[j].dataValue, currentPos] = buildTable(currentPos + tick,ruleData);
                  tick = 0;
                  #print('RETURN')
               else:
                  newTable.rows[i].colEntries[j].dataValue = ruleData[currentPos + tick];
                  #print([i,j,k,currentPos,tick,newTable.rows[i].colEntries[j].dataValue])
                  tick = tick+1;
            newTable.rows[i].colEntries[j].data = [newTable.rows[i].colEntries[j].dataType, newTable.rows[i].colEntries[j].dataValue]
   #print([currentPos,tick])
   return (newTable, currentPos + tick)


def tableReader(metaTable,outFile):
   outFile.write(str(metaTable.columnQty) + '\n')
   for i in range(metaTable.columnQty):
      outFile.write(metaTable.columnNames[i] + '\n')
   for i in range(metaTable.columnQty):
      outFile.write(metaTable.columnIndexed[i] + '\n')
   outFile.write(str(metaTable.rowQty) + '\n')
   for i in range(metaTable.rowQty):
      for j in range(metaTable.columnQty):
         outFile.write(metaTable.rows[i].colEntries[j].dataType + '\n')
         if (metaTable.rows[i].colEntries[j].dataType == 'TABLE'):
            tableReader(metaTable.rows[i].colEntries[j].dataValue,outFile)
            #print('RETURN')
         else:
            outFile.write(str(metaTable.rows[i].colEntries[j].dataValue) + '\n')


##Create File Object and open file
inputFileObject = open('FULL_CATALOG (2).met', 'r');
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
tableReader(myTable,outputFileObject)
outputFileObject.close();
