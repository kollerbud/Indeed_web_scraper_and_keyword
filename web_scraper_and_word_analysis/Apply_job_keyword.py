import requests as req
from bs4 import BeautifulSoup as soup
import time
import pandas as pd
import random
from nltk import word_tokenize, Text, FreqDist, pos_tag, ngrams
from nltk.corpus import stopwords
import sqlite3


def job_post_text(link):
    description = []
    base_url ='https://www.indeed.com'
    headers ={'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136'}
    try:
        r =req.get(base_url + link, {'User-Agent':headers}, timeout=5)
        bsobj =soup(r.content, 'html.parser')
        
        for tags in bsobj.find_all('div', {'id': 'jobDescriptionText'}):
            for litag in tags.find_all('li'):
                description.append(litag.text)
        
        if len(description)==0:
            for d in bsobj.find_all('div', {'id':'jobDescriptionText'}):
                description =d.text
                description.replace('\n', '')
        
        description =''.join(description)
        description =description.lower()

    except req.exceptions.ConnectionError as e:
        print('connection error')
        description =['connection error']
        pass
    except req.ConnectionError:
        pass

    except TypeError:
        print('watch out for "/"')
    



    return ''.join(description)


def text_analyzer(text, top_most_common=10):
    token =Text(word_tokenize(text))
    stopwords_en =set(stopwords.words('english'))
    token =[word for word in token if word.isalpha()]
    token =[word for word in token if word not in stopwords_en]

    tokens =pos_tag(token)

    verbs =[t[0] for t in tokens if t[1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']]
    freq_verbs =FreqDist(verbs).most_common(top_most_common)

    nouns =[n[0] for n in tokens if n[1] in ['NN','NNS','NNP', 'NNPS']]
    freq_nouns =FreqDist(nouns).most_common(top_most_common)

    bi_grams =list(ngrams(token,2))


    freq_bi_grams =FreqDist(ngrams(token,2)).most_common(top_most_common)

    return freq_verbs, freq_nouns,freq_bi_grams, bi_grams, token

def resume_analyzer():
    resume_text =str('''
Supply Chain Analyst
Planned and executed short-term rapid improvement initiatives at suppliers’ site, successfully improved on-time-delivery (OTD) from 40% to 90% at several key suppliers.
Mitigated delivery risks by monitored suppliers’ production planning, reviewed raw material stock and purchase schedule, and facilitated quality-related approval processes to help under-performing suppliers to achieve short-term recovery milestones.
Developed suppliers performance dashboards to analyze delivery risk, created recovery plans and coordinated with suppliers to execute corrective actions to mitigate future risks.


Supply Chain Consulting Intern
Accelerated supply chain complexity reduction by developing best practices to consolidate current direct materials suppliers count by 45%, valued at $1.3M in opportunities offset in next 3 years.
Designed strategic sourcing plans for 2019—including establishing key deliverables, creating future state roadmap and detailing execution strategy; enabled reassignment of 3 buyers within the supply chain team to focus on strategic sourcing initiatives.
Developed and onsite tested comprehensive supplier scorecard (quantitative and qualitative), which will enable supply chain team to perform effective and efficient supplier business reviews.

Process Owner				
Champion of a $750K capital expenditure project—evaluated current equipment for upgradability, identified process improvement, negotiated bids with contractors; led to a successfully funded and partially implemented multi-year project.
Deployed Six Sigma principles to support continuous improvement initiatives by established process KPIs, improved data gathering accuracy, enabled rapid response to abnormalities, which resulted in 95% first-time-yield consistently.
Identified, designed, and led two successful Kaizen events in raw material cost-saving, totaling cost-saving of $100K per year.

Application Engineering Intern					
Provided engineering concept designs and solutions to assist sales and marketing team in exploring potential new market expansion strategies, led to inception of a highly praised new product line.
Fabricated new product prototypes, benchmark functionality performance and engineering testing data to existing products to evaluate feasibility of new product introduction.

Microsoft Office Suite		Python		Tableau Power BI	SAP
Data analytics(@Github.com/kollerbud)		JD Edwards-Webi

Lean Six Sigma Green Belt
CSCP

''')
    resume_token =Text(word_tokenize(resume_text))
    stopwords_en =set(stopwords.words('english'))
    resume_token =[word for word in resume_token if word.isalpha()]
    resume_token =[word for word in resume_token if word not in stopwords_en]

    resume_token_bi_gram =list(ngrams(resume_token,2))

    return resume_token, resume_token_bi_gram

    
def comparison(job_post, resume):
    #job_post is for text analyzer
    mono_cross_word =set(job_post[4]).intersection(set(resume[0]))

    if len(job_post[4])>0:
        percent_match =str(round(len(mono_cross_word)/len(job_post[4])*100,2))
    else:
        percent_match =0
        

    return percent_match




if __name__ =='__main__':
    post_link ='www'
    k=comparison(text_analyzer(job_post_text(post_link)), resume_analyzer())
    
    print(k)
    



'''    
#######################################
    conn =sqlite3.connect('file:C:\\Users\\Li\\Desktop\\job_posts\\scrap_results.db?mode=rw', uri=True)
    c=conn.cursor()
    c.execute('SELECT job_title, company, job_link FROM scrap_results WHERE scrape_time > "20-07-04"')
    y =c.fetchall()
    print(len(y))
    query_count=0
    for row in y:
        wait =random.gauss(5,0.5)
        time.sleep(wait)
    
        k =comparison(text_analyzer(job_post_text(row[2])), resume_analyzer())
        c.execute('UPDATE scrap_results SET number_of_match=? WHERE job_title =? AND company =?', (k,row[0], row[1]))
        print(f'{query_count} updated')
        conn.commit()
        query_count +=1
    

#######################################
'''
'''
To do list:
-Add documentation for all functions
-comparison for-loop, faster way to do this?
-text_analyzer and resume_analyzer, possible to combine to optimize code speed?
--possible to combine into class
-possible utilization case for Word2vec
--ref: https://www.kaggle.com/pierremegret/gensim-word2vec-tutorial


c.execute('UPDATE scrap_results SET top_key_word="test2", number_of_match="6" WHERE job_title="Strategic Sourcing Engineer" AND company="Honeywell"')

'''