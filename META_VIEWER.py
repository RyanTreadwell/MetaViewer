# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 20:26 2018

@author: Ryan
"""

fileObject = open('CharacterCheck.met', 'r');
fileText = fileObject.read();
fileLines = fileText.split();
commonHeader = fileLines[0:13];
ruleQuantity = fileLines[14];
print commonHeader
print ruleQuantity
fileObject.close();

def Rule
