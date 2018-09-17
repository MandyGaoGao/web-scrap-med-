# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 00:35:10 2018

@author: gaoyu
"""
from xlrd import open_workbook
import openpyxl

wb = open_workbook('drug.xlsx')
ws=wb.sheet_by_index(0)
number_of_cols = ws.ncols
lst=[]
for i in range(number_of_cols-1):
    
    value  = (ws.cell(0,i).value)
    lst.append(value)

lst1=[]
for i in lst:
    name=''
    for j in i:
        if j.isupper() or j==' 'or j=='/':
            name=name+j
        else:
            break
    
    lst1.append(name)
lst2=[]
for i in lst1:
    if i[len(i)-1]==' ':
        i=i[:-1]
    lst2.append(i)

wb2 = openpyxl.load_workbook('drug.xlsx')
ws2=wb2.active
ws2.append(lst2)
wb2.save('drug.xlsx')
lst3=[]
for i in lst2:
    a=i.split('/')
    for j in a:
        lst3.append(j)
        
        
lst4=[]
for i in lst3:
    if i in lst4:
        pass
    else:
        lst4.append(i)

file = open("substance_name.txt", "w")
file.close() 
for i in lst4:
    with open("substance_name.txt", "a") as text_file:
                text_file.write(i+';')

