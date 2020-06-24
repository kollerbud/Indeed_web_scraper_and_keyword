import requests as req
from bs4 import BeautifulSoup as soup
import time
import pandas as pd
import random
import sqlite3

def get_bsobj(page_num, job_word_query='supply chain'):
    job_word_query =job_word_query.replace(' ', '+')
    base_url =f'https://www.indeed.com/jobs?q={job_word_query}&jt=fulltime&sort=date&limit=50&fromage=15&radius=25&start={page_num}'
    browser_header ={'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136'}
    web_page =req.get(base_url, {'User-Agent':browser_header})
    print(web_page.status_code)

    df =pd.DataFrame(columns=['job_title', 'job_link','company', 'location', 'company_rating', 'post_time', 'scrape_time', 'keyword'])

    bsobj =soup(web_page.content, 'lxml')

    for post in bsobj.find_all(class_='result'):

        try:
            job =post.find(class_='jobtitle', attrs={'data-tn-element':'jobTitle'})
        except:
            job =None
        try:
            company =post.find('span', class_='company').text.replace('\n', '')
        except:
            company=None
        try:
            location =post.find('span', class_='location').text
        except:
            location =None
        try:
            company_rating =post.find('a', {'class':'ratingNumber'}).text.replace('\n', '')
        except:
            company_rating=None
        try:
            post_time =post.find('div', {'class':'result-link-bar'}).find('span', {'class':'date'}).text
        except:
            post_time =None
        

        df=df.append({'job_title':job['title'], 'job_link':job['href'], 'company':company, 'location':location,
        'company_rating':company_rating, 'post_time':post_time, 'scrape_time':time.strftime('%y-%m-%d'), 'keyword':job_word_query.replace('+', ' ')}, ignore_index=True)

    return df

conn =sqlite3.connect('file:C:\\Users\\Li\\Desktop\\job_posts\\scrap_results.db?mode=rw', uri=True)

df_2 =pd.DataFrame(columns=['job_title', 'job_link','company', 'location', 'company_rating', 'post_time', 'scrape_time', 'keyword'])

for q in ['supply chain','supply chain engineer', 'supply chain analyst', 'supply chain intelligence']:
    for x in range(0,2000,50):
        #wait =2
        wait=int(random.gauss(25,5))
        time.sleep(wait)
        print(f'x: {x} query word: {q} wait time {wait}')
        df_1 =get_bsobj(x,q)
        df_1=df_1.drop_duplicates(subset=['job_link', 'job_title', 'company'], keep='first')
        df_2=pd.concat([df_2,df_1], ignore_index=True, axis=0)


df_2=df_2.drop_duplicates(subset=['job_link', 'job_title', 'company'], keep='first')
df_2.to_sql('scrap_results', con=conn, if_exists='append', index=False)
conn.commit()
conn.close()


print('change')

