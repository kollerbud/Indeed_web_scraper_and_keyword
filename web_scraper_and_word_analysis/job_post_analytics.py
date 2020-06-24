
import pandas as pd
import requests
from bs4 import BeautifulSoup as soup
import time
import random
from nltk import word_tokenize, Text, FreqDist, pos_tag, ngrams
from nltk.corpus import stopwords
import sys

def get_description(rc_link):
    desription=str('')
    headers ={'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136'}
    req =requests.get(r'https://www.indeed.com{}'.format(rc_link), {'User-Agent':headers}, timeout=5)
    bsobj =soup(req.content, 'html.parser')
    for tags in bsobj.find_all('div', {'id':'jobDescriptionText'}):
        for litag in tags.find_all('li'):
            desription += (litag.text + " ")
    
    if desription ==str(''):
        for desp in bsobj.find_all('div', {'id':'jobDescriptionText'}):
           desription =desp.text
           desription.replace('\n', '') 

    return desription.lower()


def get_noun_verb_count(desp, top_most_common=15):
    token =Text(word_tokenize(desp))
    stopwords_en =set(stopwords.words('english'))
    token =[word for word in token if word.isalpha()]
    token =[word for word in token if word not in stopwords_en]
    tokens = pos_tag(token)
    verbs =[t[0] for t in tokens if t[1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']]
    freq_verbs =FreqDist(verbs).most_common(top_most_common)
    nouns =[n[0] for n in tokens if n[1] in ['NN','NNS','NNP', 'NNPS']]
    freq_nouns =FreqDist(nouns).most_common(top_most_common)
    bi_grams =FreqDist(ngrams(token,2)).most_common(top_most_common)

    

    return print(f'top {top_most_common} verb is \n {freq_verbs}, \n top {top_most_common}  noun is \n {freq_nouns}, and \n top {top_most_common} bi-gram is \n {bi_grams}')


while True:
    try:
        user_input =input('enter job post link ')
        top =int(input('range of top keywords '))
        get_noun_verb_count(get_description(user_input), top)

    except requests.exceptions.ConnectionError as e:
        print(e, '\n retry with "/" ')
        continue

    except TypeError:
        print('enter a link')
        continue
    
    except ValueError:
        print('retry with numbers')
        continue

    search_more =input('another search? ')
    if search_more =='yes' or search_more=='Yes' or search_more=='1':
        continue
    else:
        break














    





        







        

            
            
        



    