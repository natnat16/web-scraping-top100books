# -*- coding: utf-8 -*-
"""
Web Scarping: 100 must-read classic books from Penguin pub.

@author: ANAT-H
"""
from bs4 import BeautifulSoup
import requests
import csv
import re

# send get request
URL = "https://www.penguin.co.uk/articles/2018/100-must-read-classic-books.html"
response = requests.get(URL)
response.raise_for_status()

# scrape website
website = response.text
soup = BeautifulSoup(website, "html.parser")

# get all items under cmp-text class
results = soup.select(selector=".cmp-text")

# filtering results: choosing only the items that contain the books data like so,
# option 1:
    # for each item get the first ocurrence of <p> if it starts with a number (list is numbered)
books = [item.select_one(selector="p").getText() for item in results if re.match('.?\d',item.select_one(selector="p").getText())]
# # option 2:
#   # for each item get the first ocurrence of <p> if it contains an <a> tag under <b> that is under <p>
# books = [item.select_one(selector="p").getText() for item in results if item.select_one(selector="p b a")!=None]

# writing to file
with open('top100books.csv', 'w', encoding="utf-8", newline='') as output:
  fields = ['title', 'author', 'year']  
  output_writer=csv.DictWriter(output, fieldnames=fields)
  output_writer.writeheader()
  for book in books:
    # remove extra text under <p> tag
    book = book.split('\n')[0] 
    # split string to isolate fields
    info = re.split('\d\.\s|by\xa0|\(|\)$', book) 
    # handle case when there is no year specified
    if len(info)<4:
      info.append('')
      
    book_data = {'title': info[1],
                 'author': info[2],
                 'year': info[3]
                       } 
    output_writer.writerow(book_data)

    