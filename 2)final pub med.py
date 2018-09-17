# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 17:59:56 2018

@author: gaoyu
"""


from selenium import webdriver
from bs4 import BeautifulSoup
from openpyxl import Workbook
from urllib.request import urlopen as uReq
#import webdriver.py
wb=Workbook()
rowname=['Article Link','Title','Autor','Abstract','DOI']
ws1=wb.active
ws1.append(rowname)

product=input('enter product name(e.g. asprin) here:')
kw1=input('enter keyword for 1st search here(e.g.pharmacokinectics) here:')
kw2=input('enter keyword for 2st search here(e.g.model) here:')
kw3=input('enter keyword for 3st search here(e.g.compartment) here:')
kwlist=[kw1,kw2,kw3]
def get_article_link(page):
    links=[]
    for page1 in page.find_all('div',{'class':'rslt'}):
        
        for link in page1.find_all('a'):
            #if 'Similar artciles' not in link and 'Free PMC Article' not in link.text:
            url=link.get('href')
            if url:
                if len(url)==16:
                    if '/pubmed/'in url and url[8].isdigit():
                        url='https://www.ncbi.nlm.nih.gov'+url
                        links.append(url)       
    return links

def get_article_title(page):
    links=[]
    
    for link in page.find_all('p',{'class':'title'}):  
        links.append(link.text)
    return links

def get_article_author(page):
    links=[]
    
    for link in page.find_all('p',{'class':'desc'}):  
        links.append(link.text)
    return links


def get_doi(page):
    doi_info=[]
    for link in get_article_link(page):
        
        uClient=uReq(link)
        '''download the web'''
        page_html=uClient.read()
        
        uClient.close()
        '''page parse'''
        page_soup=BeautifulSoup(page_html,'html.parser')
        for dois in page_soup.find_all('a'):
                doi=dois.get('href')
                if doi:
                    if 'doi.org' in doi:
                        doi_info.append(doi[10:])
    return doi_info
        
        
def get_abstract(page):
    info=[]
    
    for link in get_article_link(page):
        
        uClient=uReq(link)
        '''download the web'''
        page_html=uClient.read()
        
        uClient.close()
        '''page parse'''
        page_soup=BeautifulSoup(page_html,'html.parser')

        container=page_soup.find_all('div',{'class':'abstr'})
        #abstract=container.text
        text=[]
        for p in container:
            text.append(p.text)
        textstr = ''.join(text)
        info.append(textstr)
        
                
    return info
'''
def ViewBot(browser):
    
    
    ws1 = wk.add_worksheet(keyword1)           
    ws2 = wk.add_worksheet(keyword2)  
    ws3 = wk.add_worksheet(keyword3)
    wslist=[ws1,ws2,ws3]
    
    for ws in wslist:
      
    page=BeautifulSoup(browser.page_source,'html.parser')
    
    article_title=get_article_title(page)
    article_author=get_article_author(page)
    article_link=get_article_link(page)
    article_abstract=get_abstract(page)
 
    ws.append(article_link)
    ws.append(article_title)
    ws.append(article_author)
    ws.append(article_abstract)
    ws.append(get_doi(page))
    dest_filename = '{}.xlsx'.format(product)
    wb.save(filename = dest_filename)
'''
def Main():
    #parser=argparse.ArgumentParser()
    #parser.add_argument('product',help='type here the med u want')
    #parser.add_argument('keyword',help='type here the key content u want,e.g.pharmacokinetics')
    #args=parser.parse_args()
    
    #keyword=input('enter keyword for searching here:')
#r'C:/Users/gaoyu/.spyder-py3/webdriver.py'
  #  browser=webdriver.Chrome(executable_path=r'C:\Users\gaoyu\Downloads\chromedriver_win32.zip\chromedriver.exe')
    
    browser=webdriver.Chrome()
    for keyword in kwlist:
        
        browser.get('https://www.ncbi.nlm.nih.gov/pubmed/')
    
        productelement=browser.find_element_by_id('term')
        productelement.send_keys(product+' '+keyword)
  #  keywordelement=browser.find_element_by_id('fv_1')
   # keywordelement.send_keys(keyword)
        productelement.submit()
        
        page=BeautifulSoup(browser.page_source,'html.parser')
        
        article_title=get_article_title(page)
        article_author=get_article_author(page)
        article_link=get_article_link(page)
        article_abstract=get_abstract(page)
        
        ws= wb.create_sheet(keyword)

        ws.append(article_link)
        ws.append(article_title)
        ws.append(article_author)
        ws.append(article_abstract)
        ws.append(get_doi(page))
    browser.close()
    dest_filename = '{}.xlsx'.format(product)
    wb.save(filename = dest_filename)    
   

if __name__=='__main__':
    Main()
    
    

