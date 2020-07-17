from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

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
        number = header.a.get('href').split('/')[2]
        title = header.a.get_text()
        year = header.find('span', {'class' : 'lister-item-year'}).get_text().replace('(','').replace(')','').strip()
        genre = ct.find('span', {'class' : 'genre'}).get_text().replace('\n','').strip()
        star = ct.find('p', {'class' : ''}).get_text().split('\n')[-2]
      except AttributeError as e:
        print(self.url, ' : ', e)
        
        number = "!!! EROOR !!!"
        title = ""
        year = ""
        genre = ""
        star = ""
      content[number] = [title, year, genre, star]
  def setNext(self) :
    return self.bs.find('a', {'class' : 'next-page'}).get('href')

nextPage = 'https://www.imdb.com/search/title/?country_of_origin=kr&start=1351'
content = dict()

crlr = Crawler(nextPage)
bs = crlr.getPage()
parser = Parser(bs, nextPage)
parser.setContent(content)
print(content)  
# class Content:
#   def __init__(self, number, title, year, genre, star)
#     self.number = number
#     self.name = title
#     self.year = yaer
#     self.genre = genre
#     self.star = star
''' loop station
home = 'https://www.imdb.com'
nextPage = 'https://www.imdb.com/search/title/?country_of_origin=kr'
maxNum = 255
content = dict()

i = 0
while(i < maxNum) :
  crlr = Crawler(nextPage)
  bs = crlr.getPage()
  parser = Parser(bs, nextPage)
  parser.setContent(content)
  nextPage = home + parser.setNext()
  i+=1
  if (i%50 == 0) :
    print(i)
  if (i==244) :
    print(nextPage)

# print(content)
'''