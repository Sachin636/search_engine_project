import requests
from urllib.request import Request, urlopen
import bs4 
from bs4 import BeautifulSoup
import re
import os.path
import csv
import certifi
import urllib3
import PyPDF2
import io

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
    all = []
    queue.append(initial)
    count = 0
    f=open('all_links.txt','w')
    while queue:
        url = queue.pop(0)
        if '#' not in url:
            print(count , url)
            all.append(url)
            if len(all) == max_pages:
                print('Visited Max Count Pages')
                break
            f.write(url+'\n')
            count +=1
            if count == max_pages:
                break
            if url not in visited:
                visited.append(url)
                try:
                    response = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
                    page = bs4.BeautifulSoup(urlopen(response).read(), "html.parser")
                except:
                    count-=1
                    continue
                
                '''source_code = requests.get(url) 
                soup = BeautifulSoup(source_code.text,"html.parser")'''
                for link in page.findAll('a',href=True):
                    if str(link['href']).startswith('/'):
                        queue.append(str(initial[:-1])+link['href'])
                    if str(link['href']).startswith('https'):
                        queue.append(link['href'])
    f.close()
    #return visited
    
def get_html_content(url):
    print(url)
    try :
        source_code = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
        soup = bs4.BeautifulSoup(urlopen(source_code).read(),"html.parser")
    except:
        return
    save_path = 'web pages/'
    file_name = str(url).strip()
    file_name = re.sub('[^a-zA-Z0-9\s]','',file_name)
    file_name = file_name.replace('https','')
    completeName = os.path.join(save_path,file_name)
    try :
        response = urlopen(url)
    except :
        print('Exception Occured')
        return
    if 'text/html' in response.getheader('Content-Type'):
        htmlBytes = response.read()
        soup = BeautifulSoup(htmlBytes.decode('utf-8','ignore'))
        for script in soup(["script", "style"]):
                script.extract() 
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        htmlString = htmlBytes.decode("utf-8")
        #file = open(completeName,'w')
        #body_text = str(soup.body.text).encode('utf-8')
        with open(completeName, "w", encoding='utf-8') as file:
            file.write(text)
        '''file.write(text.encode('utf-8'))
        file.close()'''
        return True
    else:
        if 'application/pdf' in response.getheader('Content-Type'):
            string = ""
            r = requests.get(url)
            f = io.BytesIO(r.content)
            reader = PyPDF2.PdfFileReader(f)
            if reader.isEncrypted:
                return 
            contents =""
            for p in range(reader.getNumPages()):
                contents += reader.getPage(p).extractText()
            '''contents  = contents.encode('utf-8')
            file = open(completeName,'w')
            file.write(str(contents.decode('utf-8')))
            file.close()'''
            with open(completeName, "w", encoding='utf-8') as file:
                file.write(contents)
            return True
    
    
def clean_text():
    directory = 'web pages/'
    files = get_all_files_directory(directory)
    for i in files:
        text = open_file('web pages/'+i)
        #text = text[2:-1]
        final = []
        for word in text.split(' '):
            final.append(word)
        completeName = os.path.join(directory,i)
        file = open(completeName,'w')
        file.write(' '.join(final))

def main():
    max_page_count = 3500
    # uic_spider(3500)
    urls = []
    with open('all_links.txt') as f:
        urls=f.read().splitlines()
    urls = set(urls)
    urls = list(urls)
    dict = {}
    for i in range(len(urls)):
        dict[i+1] = urls[i]
    w = csv.writer(open("links.csv", "w"))
    for key, val in dict.items():
        w.writerow([key, val])
    for url in urls:
        get_html_content(url)
    #clean_text()
        
if __name__ == '__main__':
    main()    
