from urllib.request import urlopen
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
    html = urlopen(self.url)
    return BeautifulSoup(html, 'html.parser')

class Parser:
  def __init__(self, bs) :
    self.bs = bs
  def setContent(self, content) :
    ctList = bs.findAll('div', {'class': 'lister-item-content'})
    for ct in ctList :
      header = ct.find('h3', {'class': 'lister-item-header'})
      number = header.a.get('href').split('/')[2]
      title = header.a.get_text()
      year = header.find('span', {'class' : 'lister-item-year'}).get_text().replace('(','').replace(')','').strip()
      genre = ct.find('span', {'class' : 'genre'}).get_text().replace('\n','').strip()
      star = ct.find('p', {'class' : ''}).get_text().split('\n')[-2]
      content[number] = [title, year, genre, star]
  def setNext(self) :
    return bs.find('a', {'class' : 'next-page'}).get('href')
    

  
# class Content:
#   def __init__(self, number, title, year, genre, star)
#     self.number = number
#     self.name = title
#     self.year = yaer
#     self.genre = genre
#     self.star = star

home = 'https://www.imdb.com'
nextPage = 'https://www.imdb.com/search/title/?country_of_origin=kr'
maxNum = 20 #255
content = dict()

i = 0
while(i < maxNum) :
  crlr = Crawler(nextPage)
  bs = crlr.getPage()
  parser = Parser(bs)
  parser.setContent(content)
  nextPage = home + parser.setNext()
  i+=1

print(content)
