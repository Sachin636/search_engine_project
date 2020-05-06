import requests
import bs4 
from bs4 import BeautifulSoup
import re
import os.path
import csv

def get_all_files_directory(directory):
    """This Lists all the file in the directory"""
    file_list = os.listdir(directory)
    return file_list

def open_file(file_name):
    """Returns the content of the file"""
    f = open(file_name,"r")
    content = f.read()
    return content

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
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            response = requests.get(url, headers=headers)
            page = bs4.BeautifulSoup(response.text, "html.parser")  
            '''source_code = requests.get(url) 
            soup = BeautifulSoup(source_code.text,"html.parser")'''
            for link in page.findAll('a',href=True):
                if str(link['href']).startswith('/'):
                    queue.append(str(initial[:-1])+link['href'])
                '''if str(link['href']).startswith('https'):
                    queue.append(link['href'])'''
    return visited
    
def get_html_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    source_code = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(source_code.text,"html.parser")
    save_path = 'web pages/'
    file_name = str(soup.title.text).strip()
    file_name = re.sub('[^a-zA-Z0-9\s]','',file_name)
    completeName = os.path.join(save_path,file_name)
    file = open(completeName,'w')
    file.write(str(soup.body.text))
    file.close()
    
def clean_text():
    directory = 'web pages/'
    files = get_all_files_directory(directory)
    for i in files:
        text = open_file('web pages/'+i)
        text = text.replace('\n'," ")
        text = text.replace('Your browser is unsupported We recommend using the latest version of IE11, Edge, Chrome, Firefox or Safari.        Skip to the content of this page,','')
        completeName = os.path.join(directory,i)
        file = open(completeName,'w')
        file.write(str(text))

def main():
    max_page_count = 1
    urls = uic_spider(max_page_count)
    dict = {}
    for i in range(len(urls)):
        dict[i+1] = urls[i]
    w = csv.writer(open("links.csv", "w"))
    for key, val in dict.items():
        w.writerow([key, val])
    '''for url in urls:
        get_html_content(url)'''
    clean_text()
        
if __name__ == '__main__':
    main()    
