import os
from nltk.stem import PorterStemmer 
from nltk.corpus import stopwords 
from nltk.tokenize import RegexpTokenizer
import math
import re
from csv import reader

def get_all_files_directory(directory):
    """This Lists all the file in the directory"""
    file_list = os.listdir(directory)
    return file_list

def open_file(file_name):
    """Returns the content of the file"""
    f = open(file_name,"r")
    content = f.read()
    return content

def tokenize_space_punctuation(text):
    """Converts the given string into tokens by removing whitespace and punctuation."""
    token = RegexpTokenizer(r'[a-zA-Z]+')
    text = token.tokenize(text)
    return text

def get_stop_words():
    """Returns the stop words that are tokenized."""
    stop_words = list(stopwords.words('english'))
    text = tokenize_space_punctuation(' '.join(stop_words))
    return set(text)
    
def stemmer(text):
    """Applies stemming to all the words present in the given string."""
    text = text
    ps = PorterStemmer()
    filtered_text=[] 
    stop_words = get_stop_words()
    for word in text:
        if not word in stop_words:
            filtered_text.append(ps.stem(word))
    return filtered_text

def remove_small_words(text):
    """Removes the samll words of length 1 or 2"""
    new_text = []
    for i in text:
        if len(i) != 1 and len(i)!=2:
            new_text.append(i)
    return new_text

def get_all_text(directory):
    """Collects all the file in a directory and puts all the document contents into a single string"""
    files=get_all_files_directory(directory)
    all_text = []
    for file in files:
        text = open_file(directory + file)
        text = text.lower()
        #removed_tags = remove_tags(text)
        tokenized = tokenize_space_punctuation(text)
        stemmed = stemmer(tokenized)
        final = remove_small_words(stemmed)
        all_text.append(final)
    return all_text

def build_dictionary_posting_list(files):
    """Builds the dictionary and corresponding posting list."""
    dictionary={}
    for doc in range(len(files)):
          for token in files[doc]:
            if token in dictionary:
                if doc+1 in dictionary[token]:
                    dictionary[token][1][doc+1] += 1
                else:
                    dictionary[token][1][doc+1] = 1
                    dictionary[token][0] += 1

            else: 
                doc_dict = {}
                doc_dict[doc+1] = 1
                dictionary[token] = [1,doc_dict]
    return dictionary

def create_query(query):
    """Creates the query list of all the queries."""
    '''f = open('queries.txt',"r")
    content = f.read()
    text = content.split('\n')
    query_list = []
    for line in text:'''
    text = query.lower()
    #removed_tags = remove_tags(text)
    tokenized = tokenize_space_punctuation(text)
    stemmed = stemmer(tokenized)
    final = remove_small_words(stemmed)
    return final

def calculate_query_tf_idf(query,dictionary):
    '''calculating tf-ifd for terms in the query'''
    for word in query:
        if word not in dictionary:
            query.remove(word)
    query_word_freq = {}
    for word in query:
        if word in query_word_freq:
            query_word_freq[word] += 1
        else:
            query_word_freq[word] = 1
    s=0
    m = 0
    for word in query_word_freq.keys():
        # Remember to change this number 
        idf = math.log(48/dictionary[word][0],2)
        query_word_freq[word] *= idf
        if m<query_word_freq[word]:
            m = query_word_freq[word]
    for word in query_word_freq.keys():
        query_word_freq[word] /= m
    return query_word_freq

def calcualte_tf_docs(query,dictionary):
    '''Calulating term frquency for each word in each docs.'''
    doc_freq = {}
    for word in query:
        if word not in dictionary:
            query.remove(word)
    for n in range(1400):
        for i in query:
            if n+1 in dictionary[i][1]:
                if n+1 in doc_freq:
                    temp = {}
                    temp[i] = dictionary[i][1][n+1]
                    doc_freq[n+1].update(temp)
                else:
                    temp = {}
                    temp[i] = dictionary[i][1][n+1]
                    doc_freq[n+1] = temp
    for docs in doc_freq.items():
        m=0
        for words in docs[1]:
            docs[1][words] *= math.log(1400/dictionary[words][0],2)
            if m<docs[1][words]:
                m = docs[1][words]
        for words in docs[1]:
            docs[1][words] /= m
    return doc_freq

def create_docs_ranking(doc_freq,query_word_freq,ranks):
    """Creates the ranking of the documents based on the query and gives score to the documents."""
    docs_ranking = []
    for docs in doc_freq.items():
        doc_sum = 0
        w_sum=0
        q_sum=0
        for words in docs[1].items():
            doc_sum += words[1] * query_word_freq[words[0]]
            w_sum += words[1] 
            q_sum += query_word_freq[words[0]] 
        #doc_sum = doc_sum / math.sqrt(w_sum * q_sum) 
        docs_ranking.append([doc_sum,docs[0]])
    docs_ranking = sorted(docs_ranking,reverse = True)
    temp = docs_ranking[0:ranks]
    res = []
    for i in temp:
        res.append(i[1])
    return res

def prepare_page_dict():
    dict = {}
    with open('links.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            if row != []:
                dict[row[0]] = row[1]
    return dict
    
def vector_model(input):
    directory = 'web pages/'
    files = get_all_text(directory)
    dictionary = build_dictionary_posting_list(files)
    query = create_query(input)
    query_df_idf = calculate_query_tf_idf(query,dictionary)
    doc_df_idf = calcualte_tf_docs(query,dictionary)   
    ranking = create_docs_ranking(doc_df_idf,query_df_idf,10)
    dict = prepare_page_dict()
    result = []
    for i in ranking:
        result.append(dict[str(i)])
    return result
    
if __name__ == "__main__":
    main()