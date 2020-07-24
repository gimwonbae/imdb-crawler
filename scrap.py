from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
# import csv
import re
from pandas import DataFrame

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
  def saveHtml(self, path):
    try:
      html = urlopen(self.url)
      # print(path + self.url.replace('/','-') + '.html')
      f= open(path + self.url.replace('https://','').replace('/','-').replace('?','Q') + '.html', 'wb')
      f.write(html.read())
    except HTTPError as e:
      print(self.url, ' : ', e)
    

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
        title = header.a.get_text().strip()
      except AttributeError as e:
        title = ''
        # print(self.url, ' : TITLE ', e)
      try:
        yearNotClean = header.find('span', {'class' : 'lister-item-year'}).get_text().replace('(','').replace(')','').strip()
        if 'Video Game' in yearNotClean:
          year = 'Video Game'
        else:
          year = re.sub('[^0-9–]', '', yearNotClean)  
      except AttributeError as e:
        year = ''
        # print(self.url, ' : YEAR ', e)            
      # try:
      #   tv = 
      # except AttributeError as e:

      try:  
        genre = ct.find('span', {'class' : 'genre'}).get_text().replace('\n','').strip()
      except AttributeError as e:
        genre = ''
        # print(self.url, ' : GENRE ', e)
      try:
        items = nextSib(ct.find('p'), 6).get_text().split('\n')
        i = 0
        star = ''
        for item in items:
          if 'Star' in item:
            star = items[i+1].replace(',','').strip()
            break
          i+=1
      except AttributeError as e:
        star = ''
        # print(self.url, ' : STAR ', e)
        
      try:
        crlr = Crawler('https://www.imdb.com/title/' + number)
        bs2 = crlr.getPage()
        moreYear = bs2.find('a', {'title' : 'See more release dates'}).get_text()
        if 'TV Series' in moreYear:
          TVseries = True
        else:
          TVseries = False
      except AttributeError as e:
        TVseries = ''
        # print(self.url, ' : TVseries', e) 

      file = self.url.replace('https://','').replace('/','-').replace('?','Q') + '.html'

      content['number'].append(number)
      content['title'].append(title)
      content['year'].append(year)
      content['genre'].append(genre)
      content['star'].append(star)
      content['TVseries'].append(TVseries)
      content['file'].append(file)

  def setNext(self) :
    try:
      url = self.bs.find('a', {'class' : 'next-page'}).get('href')
    except AttributeError as e:
      url = ''
    return url
    
# def makeCsv(content) :
#   csvFile = open('test.csv', 'w+', encoding='utf-8')
#   try:
#     writer = csv.writer(csvFile)
#     writer.writerow(('id','title','year','genre','star'))
#     for key, value in content.items():
#       writer.writerow((key, value[0], value[1], value[2], value[3]))
#   finally:
#     csvFile.close()

def toExcel(content) :
  df = DataFrame(data=content, columns=['number','title','year','genre','star','TVseries','file'])
  df = df.drop_duplicates('number')
  df = df.drop(df[df['year'].str.contains('Video Game')].index)
  df.to_excel("test.xlsx")

# class Content:
#   def __init__(self, number, title, year, genre, star)
#     self.number = number
#     self.name = title
#     self.year = yaer
#     self.genre = genre
#     self.star = star

home = 'https://www.imdb.com'
# nextPage = 'https://www.imdb.com/search/title/?country_of_origin=kr&start=5001'
nextPage = 'https://www.imdb.com/search/title/?country_of_origin=kr'
maxNum = 1000
content = {'number':[] ,'title':[],'year':[],'genre':[],'star':[], 'TVseries':[], 'file':[]}

i = 0
while(i < maxNum) :
  crlr = Crawler(nextPage)
  bs = crlr.getPage()
  crlr.saveHtml('C:\\Project\\20200717_crawler\\html\\')
  parser = Parser(bs, nextPage)
  parser.setContent(content)
  # print(i)
  nextUrl = parser.setNext()
  if (not nextUrl):
    break
  else:
    nextPage = home + nextUrl
  i+=1
  # if (i==255) :
  #   print(nextPage)
# print(content)
toExcel(content)