from nltk.stem import PorterStemmer 
import re
from csv import reader
from nltk import word_tokenize
from collections import OrderedDict
from operator import itemgetter   
from nltk.util import ngrams
from collections import Counter
from itertools import chain
import random
import os

def stemmer(text):
    """Applies stemming input text."""
    ps = PorterStemmer()
    return ps.stem(text)

def open_file(file_name):
    """Returns the content of the file"""
    f = open(file_name,"r",encoding='iso-8859-15')
    content = f.read()
    return content

def word_graph(file_content):
    ''' Funtion to load the given documnent in the undirected word graph 
    It takes text as input and creates undirected graph for it.''' 
    w = 5
    count = 0
    graph = {}
    original_text = []
    for word in word_tokenize(file_content):
        if len(word)>2:
                    k =stemmer(word)
                    graph[k]=[[],0]
                    original_text.append(k)
    for i in range(len(original_text)):
        if original_text[i] in graph.keys():
            for j in range(1,w+1):
                if i+j<len(original_text) and original_text[i+j] in graph.keys():
                    if original_text[i+j] not in graph[original_text[i]][0]: 
                        graph[original_text[i]][0].append(original_text[i+j])
                    if original_text[i] not in graph[original_text[i+j]][0]:
                        graph[original_text[i+j]][0].append(original_text[i])
    return graph,len(original_text),' '.join(original_text)  

def word_page_rank(graph,length):
    '''This method takes the graph and appies the page rank eqaution 
    to the each node on the graph.'''
    damping_factor = 0.90
    for keys in graph.keys():
        graph[keys][1] = 1/length
    iteration = 10
    for i in range(iteration):
        node = list(graph.keys())[random.randrange(0,len(graph.keys()))]
        node_sum = 0
        for i in graph[node][0]:
            temp=graph[i][1]
            denominator = 0
            for j in graph[i][0]:
                denominator+=graph[j][1]
            node_sum+=(temp/denominator)*graph[node][1]   
        graph[node][1]=(damping_factor * node_sum)+((1-damping_factor)*(1/length))
    return graph
       
def calculates_rank(query,graph):
    '''This fuction takes the text and creates the ngrams using the nltk nbgram library.'''
    all_words = word_tokenize(query)
    stemmed_query = []
    for word in all_words:
        if len(word)>2:
                k=stemmer(word)
                stemmed_query.append(k)
    # Here filtering of the ngrams takes place
    # rules for the key phrases
    #all_grams = chain(unigrams,bigrams) 
    total_weight = {}
    for word in stemmed_query: 
        temp = 0
        if word in graph.keys():
                temp+=graph[word][1]
        total_weight[word]=temp
    sum = 0
    for key in total_weight.keys():
        sum += total_weight [key]      
    return sum

def get_all_files_directory(directory):
    """This Lists all the file in the directory"""
    file_list = os.listdir(directory)
    return file_list

def prepare_page_dict():
    dict = {}
    with open('links.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            if row != []:
                dict[row[0]] = row[1]
    return dict

def page_rank_by_words(query):
    directory = 'web pages/'
    files = get_all_files_directory(directory)
    count = 1
    res= [] 
    for file in files:
        file_text = open_file('web pages/'+file)
        initial = word_graph(file_text)
        final_graph = word_page_rank(initial[0],initial[1])
        res.append([calculates_rank(query,final_graph),count])
        count+=1
    res = sorted(res,reverse=True)
    top_10 = []
    for i in range(10):
        top_10.append(res[i][1])
    ranking = top_10
    dict = prepare_page_dict()
    result = []
    for i in ranking:
        result.append(dict[str(i)])
    return result
