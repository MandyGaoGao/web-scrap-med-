# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 20:09:27 2018

@author: gaoyu
"""

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import csv
import time
from itertools import islice
from openpyxl import Workbook
wb=Workbook()

start_time = time.time()

def dicfromcsv(csvfile):
    reader = csv.reader(open(csvfile, 'r'))
    d = {}
    for row in islice(reader,0,28800):
        try:
            k,v = row
            d[k] = v
        except:
            pass
    return d

def getabstract(url):
    try:
        uClient=uReq(url)
        page_html=uClient.read()
        uClient.close()
        page_soup=soup(page_html,'html.parser')
        
        
        a=page_soup.find(string=re.compile("PROPRIETES PHARMACOLOGIQUES")) 
        b=page_soup.find(string=re.compile("DONNEES PHARMACEUTIQUES")) 
        b_position=articletext.index(b)
        a_position=articletext.index(a)
        #print(a_position,b_position)
        descrip=str(articletext[int(a_position):int(b_position)])
        
    except:
        
        num=url[73:81]
        descrip='http://base-donnees-publique.medicaments.gouv.fr/extrait.php?specid='+num
 
    return descrip
def Main():
    ls1=[] 
    ls2=[]
    ls3=[]
    
    d=dicfromcsv('RCP index.csv')
    for i in d.keys():
        ls1.append(i)
        ls2.append(d[i])
        ls3.append(getabstract(d[i]))
    
    
    ws=wb.active
    
        
    ws.append(ls1)
    ws.append(ls2)
    ws.append(ls3)
    wb.save('RCP index-extract(modified).xlsx')
   
'''    
    ws=wb.active()
    row = 0
    col = 0 
    for key in d.keys():
        row += 1
        ws.write(row, col, key)  
        ws.write(row, col + 1, getabstract(d[key])
    wb.save('RCP index.xlsx')
    
'''    
if __name__=='__main__':
    Main()               
print("--- %s seconds ---" % (time.time() - start_time))              
                