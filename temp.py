from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
url = 'https://www.cs.uic.edu'
req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
print(webpage)