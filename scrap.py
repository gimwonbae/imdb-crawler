from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd

def nextSib(head, number):
    i = 0
    sib = head
    while(i < number):
      sib = sib.next_sibling
      i += 1
    return sib

class Crawler:
  def __init__(self, url):
    self.url = url
  def getPage(self):
    try:
      html = urlopen(self.url)
    except HTTPError as e:
      print(self.url, ' : ', e)
    return BeautifulSoup(html, 'html.parser')

class Parser:
  def __init__(self, bs, url) :
    self.bs = bs
    self.url = url
  def setContent(self, content) :
    ctList = self.bs.findAll('div', {'class': 'lister-item-content'})
    for ct in ctList :
      try:
        header = ct.find('h3', {'class': 'lister-item-header'})
      except AttributeError as e:
        header = ''
        # print(self.url, ' : HEADER ', e)  
      try:
        number = header.a.get('href').split('/')[2]
      except AttributeError as e:
        number = ''
        # print(self.url, ' : NUMBER ', e)
      try:
        title = header.a.get_text()
      except AttributeError as e:
        title = ''
        # print(self.url, ' : TITLE ', e)
      try:
        year = header.find('span', {'class' : 'lister-item-year'}).get_text().replace('(','').replace(')','').strip()
      except AttributeError as e:
        year = ''
        # print(self.url, ' : YEAR ', e)
      try:  
        genre = ct.find('span', {'class' : 'genre'}).get_text().replace('\n','').strip()
      except AttributeError as e:
        genre = ''
        # print(self.url, ' : GENRE ', e)
      try:
        star = ct.find('p', {'class' : ''}).get_text().split('\n')[-2]
      except AttributeError as e:
        star = ''
        # print(self.url, ' : STAR ', e)
      content['number'].append(number)
      content['title'].append(title)
      content['year'].append(year)
      content['genre'].append(genre)
      content['star'].append(star)

  def setNext(self) :
    return self.bs.find('a', {'class' : 'next-page'}).get('href')
    
def makeCsv(content) :
  csvFile = open('test.csv', 'w+', encoding='utf-8')
  try:
    writer = csv.writer(csvFile)
    writer.writerow(('id','title','year','genre','star'))
    for key, value in content.items():
      writer.writerow((key, value[0], value[1], value[2], value[3]))
  finally:
    csvFile.close()

# class Content:
#   def __init__(self, number, title, year, genre, star)
#     self.number = number
#     self.name = title
#     self.year = yaer
#     self.genre = genre
#     self.star = star

home = 'https://www.imdb.com'
nextPage = 'https://www.imdb.com/search/title/?country_of_origin=kr'
maxNum = 10
content = {'number':[] ,'title':[],'year':[],'genre':[],'star':[]}

i = 0
while(i < maxNum) :
  crlr = Crawler(nextPage)
  bs = crlr.getPage()
  parser = Parser(bs, nextPage)
  parser.setContent(content)
  nextPage = home + parser.setNext()
  i+=1
  # if (i==255) :
  #   print(nextPage)

print(content)
# makeCsv(content)