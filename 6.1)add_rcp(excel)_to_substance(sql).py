# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 18:34:45 2018

@author: gaoyu
"""

import pandas as pd
import pyodbc
#set up one sql table by manually import one excel or create database manually

#get list of info from new excel
file='toadd(substance)'
a=pd.read_excel('{}.xlsx'.format(file))
names=a.columns

lst1=[]
for i in a.index:
    lst=[]
    for name in names:
        lst.append(str(a[str(name)][i]))
    lst1.append(lst)
print(lst1)
# make connection to sql and populate

#connection = pyodbc.connect(r'Driver={SQL Server};Server=localhost;Database=equation;Trusted_Connection=yes;')
connection=pyodbc.connect(r'Driver={SQL Server};SERVER=exactcurefirstdb.cb9zgxqtumuv.eu-west-1.rds.amazonaws.com;DATABASE=RCPequation;UID=mbexactcure;PWD=ExactCurePower42')
cursor = connection.cursor()

SQLCommand = ("INSERT INTO dbo.substance "
                 "(substance_name,F,t12,tmax,Vd,Cmax,CL) "
                 "VALUES (?,?,?,?,?,?,?)")

for i in lst1:  
    Values =i
    cursor.execute(SQLCommand,Values) 

connection.commit() 
connection.close()




