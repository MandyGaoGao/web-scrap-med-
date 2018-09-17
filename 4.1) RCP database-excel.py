# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 21:55:03 2018

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

def getsubstance(url):
    try:
        uClient=uReq(url)
        page_html=uClient.read()
        uClient.close()
        page_soup=soup(page_html,'html.parser')        
        articletext=page_soup.text

        a1=re.search(r'\b(Composition)\b', articletext)
        a2=re.search(r'\b(Présentations)\b',articletext)
        b1=a1.start()+39
        b2=a2.start()
        sub=articletext[b1:b2]
        ls=sub.split('>')
#sub=sub.replace(' ','')
        ls1=[]
        ls2=[]
        for i in ls:
            i=i.replace('>','')
            
            i=i.replace('\t','')
            i=i.replace('\r','')
            i=i.replace('\n','')
            ls1.append(i)

#a=page_soup.find_all('div',{'class':'compoMain'})
        
        substance=''
        for i in ls1[1:]:
            substance=substance+i


        ls2.append(ls1[0])
        ls2.append(substance)
        return ls2
    except:
        sub='na'
    return sub

# d: k is the product name;v is the product link of rcp
def dicfromcsv(csvfile):
    reader = csv.reader(open(csvfile, 'r'))
    d = {}
    for row in islice(reader,0,5):
        try:
            k,v = row
            d[k] = v
        except:
            pass
    return d

#n=0,name; n=1,form    
def seperate(title,n):
    lst=title.split(',')
    name=lst[n]
    return name





def getabstract(url):
    try:
        uClient=uReq(url)
        page_html=uClient.read()
        uClient.close()
        page_soup=soup(page_html,'html.parser')
        
        articletext=page_soup.text
        a=page_soup.find(string=re.compile("Propriétés pharmacocinétiques")) 
        b=page_soup.find(string=re.compile("5.3. Données de sécurité préclinique")) 
        b_position=articletext.index(b)
        a_position=articletext.index(a)
        descrip1=str(articletext[int(a_position):int(b_position)])
        
        c=page_soup.find(string=re.compile("Posologie et mode d'administration")) 
        d=page_soup.find(string=re.compile("4.3. Contre-indications")) 
        c_position=articletext.index(c)
        d_position=articletext.index(d)
        descrip2=str(articletext[int(c_position):int(d_position)])
        
        descrip=descrip1+'\n'+descrip2 
    except: 
        descrip='PDF'
    return descrip


def Main():
    ls1=[] 
    ls2=[]
    ls3=[]
    ls=[]
    ls4=[]
    formlst=[]
    d=dicfromcsv('3.2)RCP index.csv')
    for i in d.keys():
        #productname
        ls1.append(seperate(i,0))
        #form
        ls2.append(seperate(i,1))
        ls.append(getsubstance('http://base-donnees-publique.medicaments.gouv.fr/extrait.php?specid='+d[i][73:81])[1])
        
        ls3.append('http://base-donnees-publique.medicaments.gouv.fr/extrait.php?specid='+d[i][73:81])
        #get RCP4.2 5.2
        ls4.append(getabstract(d[i]))
    
    
    ws=wb.active
    
        
    ws.append(ls1)
    ws.append(ls2)
    ws.append(ls)
    ws.append(ls3)
    ws.append(ls4)
    wb.save('RCP data (0,1000).xlsx')
   
  
if __name__=='__main__':
    Main()               
print("--- %s seconds ---" % (time.time() - start_time))      
