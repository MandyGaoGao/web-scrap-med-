# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 15:37:38 2018

@author: gaoyu
"""
from urllib.request import urlopen as uReq

from bs4 import BeautifulSoup as soup
import re
from openpyxl import Workbook
wb=Workbook()


'''urllib grab, bs4 copy html text'''

lstA=range(999)
lstB=[]
for i in lstA:
    lstB.append(str(i))

lst1=[]
lst2=[]

for number in lstB:
    try:
        my_url = 'http://base-donnees-publique.medicaments.gouv.fr/affichageDoc.php?specid=6000'+number+'&typedoc=R'
    #lst=range(9)
    #listofurl=['http://base-donnees-publique.medicaments.gouv.fr/affichageDoc.php?specid=64207990&typedoc=R']
    #for my_url in listofurl:   
        uClient=uReq(my_url)
        '''download the web'''
        page_html=uClient.read()
        
        uClient.close()
        '''page parse'''
        page_soup=soup(page_html,'html.parser')
        
        container=page_soup.find('div',id="textDocument")
        articletext=page_soup.text
        a=page_soup.find(string=re.compile("PROPRIETES PHARMACOLOGIQUES")) 
        b=page_soup.find(string=re.compile("DONNEES PHARMACEUTIQUES")) 
        b_position=articletext.index(b)
        a_position=articletext.index(a)
        #print(a_position,b_position)
        descrip=str(articletext[int(a_position):int(b_position)])
    
        lst1.append(descrip)
        
        
        
        product_name1=page_soup.title.text
        product_name2=product_name1.replace('Résumé des caractéristiques du produit - ','')
        product_name=product_name2.replace('  - Base de données publique des médicaments','')
        
        lst2.append(str(product_name))
    except:
        pass
        
    #print(product_name)
    #csv_file=open('pharmaresume.csv','w')
ws=wb.active
ws.append(lst2)
ws.append(lst1)
wb.save('pharmaresumeexcel.xlsx')


'''
csv_file = open("pharmaresume1.csv", 'a',  newline='', encoding='utf-8')
csv_writer=csv.writer(csv_file)

csv_writer.writerow(lst2)
csv_writer.writerow(lst)
csv_file.close()
'''
                