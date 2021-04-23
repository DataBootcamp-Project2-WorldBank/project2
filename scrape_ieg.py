#!/usr/bin/env python
# coding: utf-8

# Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import re

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# URL of page to be scraped nasa mars news
url = 'https://finances.worldbank.org/Other/IEG-World-Bank-Project-Performance-Ratings/rq9d-pctf'
browser.visit(url)
html = browser.html
soup = bs(html, 'html.parser')
#print(soup.prettify())

# get news title, news link, news text, news date
results = soup.find_all("div", attrs={"class":"socrata-table"})

table = results[0].find("table")

body = table.find_all("tr")
head=body[0]
body_rows=body[1:]
headings=[]
for item in head.find_all("th"):
    item=(item.text).rstrip("\n")
    headings.append(item)
#print(headings)

all_rows = [] # will be a list for list for all rows
for row_num in range(len(body_rows)): # A row at a time
    row = [] # this will old entries for one row
    for row_item in body_rows[row_num].find_all("td"): #loop through all row entries
        # row_item.text removes the tags from the entries
        # the following regex is to remove \xa0 and \n and comma from row_item.text
        # xa0 encodes the flag, \n is the newline and comma separates thousands in numbers
        aa = re.sub("(\xa0)|(\n)|,","",row_item.text)
        #append aa to row - note one row entry is being appended
        row.append(aa)
    # append one row to all_rows
    all_rows.append(row)

df = pd.DataFrame(data=all_rows,columns=headings)

df.columns=['Project ID','Project Name','Region','Country Code','Country Name','Approval Date',
       'Approval FY','Sector Board','Agreement Type','Lending Project Cost','Net Commitment',
       'Deactivation Date','Exit FY','Lending Instrument Typen','Lending Instrument','Product Line Code',
       'Product Line','IEG_EvalDate','IEG_EvalFY','IEG_EvalType','ERR at Appraisal','ERR at Completion',
       'IEG_Outcome','IEG_RDO','(disc)IEG_IDImpact','IEG_BankQualityAtEntry','IEG_BankQualityOfSupervision',
       'IEG_OverallBankPerf','(disc)IEG_BorrPrep','EG_ImplementingAgencyPerf','IEG_GovernmentPerf',
       'IEG_OverallBorrPerf','IEG_ICRQuality','(disc)IEG_Sustainability','IEG_MEQualit','IEG_SourceDocumentURL']

df.to_html('app/templates/ieg_table.html')

browser.quit()




