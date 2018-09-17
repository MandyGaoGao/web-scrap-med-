# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 18:12:56 2018

@author: gaoyu
"""

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv


import time
start_time = time.time()


def get_article_link(page):
    dic={}
    for article in page.find_all('a',{'class':'standart'}):
        product=article.text
        url=article.get('href')
        if url:
            if 'extrait.php?specid='in url:
                url='http://base-donnees-publique.medicaments.gouv.fr/affichageDoc.php?specid='+url[19:]+'&typedoc=R'
                dic[str(product.replace('\t\t\t\t',''))]=url     
    
    return dic

def Main():
    w = csv.writer(open("RCP index.csv", "w"))
    try:
        for i in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
    
            my_url = 'http://base-donnees-publique.medicaments.gouv.fr/liste-medicaments-'+i+'.php'
            uClient=uReq(my_url)
            page_html=uClient.read()
            uClient.close()
            page_soup=soup(page_html,'html.parser')
            dic=get_article_link(page_soup)
            for key, val in dic.items():
                w.writerow([key, val])
    except:
        pass

if __name__=='__main__':
    Main()
    
print("--- %s seconds ---" % (time.time() - start_time))
        
       
    
