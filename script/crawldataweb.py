# -*- coding: utf-8 -*-
"""CrawlDataWeb.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HW4UfSPsHYCYyLxSh7_HvERrAJWO-Duc

# Library
"""

# requests for fetching html of website
import requests

import re
from bs4 import BeautifulSoup, SoupStrainer
import requests

from urllib.request import urlopen

import pandas as pd

from google.colab import drive
drive.mount('/content/gdrive/')

import io, os, sys

"""# General function"""

# Find true link from a website

def find_true(page_size, url, keyword, before_term, after_term):
  true_link = []
  for i in range(page_size):
    page = requests.get(url[i])    
    data = page.text
    soup = BeautifulSoup(data)
    all_link = soup.find_all('a')
    for link in all_link:
      raw_link = link.get('href')
      raw_link = str(raw_link)
      search = re.search(keyword, raw_link)
      if search:
        raw_link = before_term + raw_link + after_term
        if raw_link not in true_link:
          true_link.append(raw_link)
  return true_link  


# Extract content from a url  

def extract_content(url, exclude, tag, attribute):
  true_text = ''
  try:
    html = urlopen(url)
    content = BeautifulSoup(html)
    if len(attribute) == 0: 
      all_text = content.find_all(tag)
    else:
      all_text = content.find_all(tag, attrs={"class":attribute})
    for texts in all_text:
      raw_text = str(texts.text)
      for char in exclude:
        raw_text = raw_text.replace(char, " ")
      true_text = true_text + ' ' + raw_text
  except: 
    true_text = 'No content found to extract.'
  return true_text


# Save content from a website

def save_content(page, exclude, tag, attribute):
  size = len(page)
  contents = []
  for i in range(size):
    content = extract_content(page[i], exclude, tag, attribute)
    contents.append(content)
  return contents


# Create dataframe to save content extracted

def create_df(page_name, page_link, page_content):
  df = pd.DataFrame({'Name': page_name, 'Link': page_link, 'Content': page_content},
                    columns = ['Name', 'Link', 'Content'])
  return df

#Create a input data folder to store crawling data

my_path = "/content/gdrive/My Drive/KindProject_InputData/"
data_path = os.path.join(my_path, 'CrawlingResult/')

# Combine data

kindmate = create_df('Kindmate', kindmate_link, kindmate_content)
nhidong = create_df('Nhidong', nhidong_link, nhidong_content)
heart4u = create_df('Heart4u', heart4u_link, heart4u_content)
data_crawl = pd.concat([kindmate, nhidong, heart4u], ignore_index = True)

# Save current data file

list_files = os.listdir(data_path)
for file in list_files:
  if file == 'crawl_content.csv':
    os.rename(data_path + file, data_path + 'crawl_content_old.csv')

    
#Import crawl data to new csv file

with open (os.path.join(data_path, "crawl_content.csv"), "w") as myfile:
    data_crawl.to_csv(myfile, encoding = 'utf-8')
    status = 'New'

    
#Delete ole file if new file created  

list_files = os.listdir(data_path)
for file in list_files:
  if status == 'New':
    if file == 'crawl_content_old.csv':
      os.remove(data_path + file)

"""# Kindmate Website"""

#kindmate

kindmate_url = []
kindmate_keyword = '/project/'
kindmate_size = 30
for i in range(kindmate_size):
  j = i + 1
  kindmate_url.append("https://kindmate.net/explore?page=" + str(j))

kindmate_link = find_true(kindmate_size, kindmate_url, kindmate_keyword, '', '')
kindmate_exclude = ['\r\n', '\n', '\xa0', '++', '❤️', '&quot']
kindmate_content = save_content(kindmate_link, kindmate_exclude, 'p', [])
kindmate_content

"""# Nhidong Website"""

#nhidong.org
 
nhidong_size = 1
nhidong_url = []
nhidong_url.append("http://nhidong.org.vn/cong-tac-xa-hoi-c1061.aspx")
nhidong_keyword = '/chuyen-muc/'
nhidong_link = find_true(nhidong_size, nhidong_url, nhidong_keyword, "http://nhidong.org.vn", '')
nhidong_tag = 'div'
nhidong_attribute = ['col-md-12 des-ct', 'row content-news']
nhidong_exclude = ['\n', '\xa0']
nhidong_content = save_content(nhidong_link, nhidong_exclude, nhidong_tag, nhidong_attribute)
nhidong_content

"""# Traitimchoem Website"""

#Trai tim cho em

heart4u_url = []
heart4u_url.append('http://traitimchoem.vn/ho-so')
heart4u_keyword = 'http://traitimchoem.vn/ho-so/'
heart4u_size = 36
for i in range(heart4u_size):
  j = i + 2
  heart4u_url.append('http://traitimchoem.vn/ho-so/page:' + str(j))

heart4u_size = len(heart4u_url)
heart4u_link = find_true(heart4u_size, heart4u_url, heart4u_keyword, '', '')

heart4u_exclude = ['<div class="col-sm-3 col-xs-6">', '</div>', '\n']
heart4u_tag = 'div'
heart4u_attribute = ['col-sm-9', 'col-sm-3 col-xs-6', 'col-sm-9 col-xs-6']

heart4u_content = save_content(heart4u_link, heart4u_exclude, heart4u_tag, heart4u_attribute)
heart4u_content

"""#Data Storing

Save all crawled data to a csv file into google drive.
"""

#Create a input data folder to store crawling data

my_path = "/content/gdrive/My Drive/"
data_path = os.path.join(my_path, 'KindProject_InputData/')

# Combine data

kindmate = create_df('Kindmate', kindmate_link, kindmate_content)
nhidong = create_df('Nhidong', nhidong_link, nhidong_content)
heart4u = create_df('Heart4u', heart4u_link, heart4u_content)
data_crawl = pd.concat([kindmate, nhidong, heart4u], ignore_index = True)

# Save current data file

list_files = os.listdir(data_path)
for file in list_files:
  if file == 'crawl_content.csv':
    os.rename(data_path + file, data_path + 'crawl_content_old.csv')
    
#Import crawl data to new csv file

with open (os.path.join(data_path, "crawl_content.csv"), "w") as myfile:
  data_crawl.to_csv(myfile, encoding = 'utf-8')
  status = 'New'

    
#Delete ole file if new file created  

if status == 'New':
  list_files = os.listdir(data_path)
  for file in list_files:
      if file == 'crawl_content_old.csv':
        os.remove(data_path + file)