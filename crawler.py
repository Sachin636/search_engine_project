import requests
from bs4 import BeautifulSoup
import re
import os.path

def uic_spider(max_pages):
    '''This method will crawl over the web pages.
    Crawling will be done in  a bfs method.'''
    initial  = 'https://cs.uic.edu/'
    page = 1
    queue = []
    visited = []
    queue.append(initial)
    count = 0
    while queue:
        url = queue.pop(0)
        count +=1
        if url not in visited:
            visited.append(url)
            source_code = requests.get(url) 
            soup = BeautifulSoup(source_code.text,"html.parser")
            for link in soup.findAll('a',href=True):
                if str(link['href']).startswith('/'):
                    queue.append(str(initial[:-1])+link['href'])
                '''if str(link['href']).startswith('https'):
                    queue.append(link['href'])'''
    return visited
    
def get_html_content(url):
    source_code = requests.get(url) 
    soup = BeautifulSoup(source_code.text,"html.parser")
    save_path = 'web pages/'
    file_name = str(soup.title.text).strip()
    file_name = re.sub('[^a-zA-Z0-9\s]','',file_name)
    completeName = os.path.join(save_path,file_name)
    file = open(completeName,'w')
    file.write(str(soup.body.text))
    file.close()

def main():
    max_page_count = 1
    urls = uic_spider(max_page_count)
    for url in urls:
        get_html_content(url)
        
if __name__ == '__main__':
    main()    
