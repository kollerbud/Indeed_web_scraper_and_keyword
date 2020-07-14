import requests as req
from bs4 import BeautifulSoup as soup
import time
import pandas as pd
import random
import sqlite3
import Apply_job_keyword as apply
def get_bsobj(page_num, job_word_query='supply chain'):
    job_word_query =job_word_query.replace(' ', '+')
    base_url =f'https://www.indeed.com/jobs?q={job_word_query}&jt=fulltime&sort=date&limit=50&fromage=15&filter=1&radius=25&start={page_num}'
    browser_header ={'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
    
    }
    web_page =req.get(base_url, {'User-Agent':browser_header}, timeout=10)
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
            location =post.find('span', attrs={'class':'location accessible-contrast-color-location'}).text
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
        'company_rating':company_rating, 'post_time':post_time, 'scrape_time':time.strftime('%y-%m-%d'), 'keyword':job_word_query.replace('+', ' '), 'number_of_match':None}, ignore_index=True)

    return df


df_2 =pd.DataFrame(columns=['job_title', 'job_link','company', 'location', 'company_rating', 'post_time', 'scrape_time', 'keyword', 'number_of_match'])
today =time.strftime('%Y-%m-%d')
for q in ['supply chain','supply chain engineer', 'supply chain analyst', 'supply chain intelligence', 'operations analyst']:
    for x in range(0,1050,50):
        #wait =2
        wait=int(random.gauss(5,1))
        time.sleep(wait)
        print(f'x: {x} query word: {q} wait time {wait}')
        df_1 =get_bsobj(x,q)
        df_1=df_1.drop_duplicates(subset=['job_link', 'job_title', 'company'], keep='first')
        df_2=pd.concat([df_2,df_1], ignore_index=True, axis=0)
df_2=df_2.drop_duplicates(subset=['job_title', 'company'], keep='first')
#df_2.to_csv(f'C:\\Users\\Li\Desktop\\job_posts\\{today}_.csv', index=False)


#save scrape results just in case program got interrupted
today =time.strftime('%Y-%m-%d')
df_2.to_csv(f'C:\\Users\\Li\Desktop\\job_posts\\{today}.csv')

'''
########psudo value to test#############
today =time.strftime('%Y-%m-%d')
df_2 =pd.read_csv(f'C:\\Users\\Li\Desktop\\job_posts\\{today}.csv', index_col=False)

#df_2 =df_test[:10]
#############################
df_2=df_2.drop_duplicates(subset=['job_title', 'company'], keep='first')
print(f'{len(df_2)} links to go through')
'''

df_2 =df_2.drop_duplicates(subset=['job_title', 'company'], keep='first')

error_point=0
df_2 =df_2[error_point:]
print(f'{len(df_2)} links to go through')

for counter, link in enumerate(df_2['job_link']):
    try:
        wait=int(random.gauss(5,1))
        time.sleep(wait)
        k =apply.comparison(apply.text_analyzer(apply.job_post_text(link)), apply.resume_analyzer())
        df_2.iloc[counter, 8] =k
        print(f'counter {counter}, k {k}')
        if counter % 100 ==0 and counter >0:
            df_2.iloc[counter-99:counter, :].to_csv(f'C:\\Users\\Li\Desktop\\job_posts\\{today}_{str(counter+error_point)}.csv', index=False)
            print(f'{counter-99} to {counter} csv made')
    except req.exceptions.ReadTimeout:
        df_2.loc[counter, 'number_of_match'] ='error timeout'
        print('timeout error occur')
        continue

conn =sqlite3.connect('file:C:\\Users\\Li\\Desktop\\job_posts\\scrap_results.db?mode=rw', uri=True)
df_2.to_sql('scrap_results', con=conn, if_exists='append', index=False)
conn.commit()
conn.close()