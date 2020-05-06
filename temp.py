import requests
import bs4
import os

def get_all_files_directory(directory):
    """This Lists all the file in the directory"""
    file_list = os.listdir(directory)
    return file_list

def open_file(file_name):
    """Returns the content of the file"""
    f = open(file_name,"r")
    content = f.read()
    return content

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
    
clean_text()