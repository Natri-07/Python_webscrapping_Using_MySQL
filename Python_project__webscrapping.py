# Web__Scrapping.py
from bs4 import BeautifulSoup
import requests

import mysql.connector as sql
connect = sql.connect(host="localhost", user="Naveen", passwd="75860609", database="web_scrapping")
cursor = connect.cursor()
if connect.is_connected():
    print("Connected to MySQL Server")

print("Enter the skills that you are not familiar with: ")
unfamiliar_skill = input('>')
print(f'Filtering Out{unfamiliar_skill}')

def find_jobs():
    html_text = requests.get("https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=").text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    for job in jobs:
            company_name = job.find('h3',class_ = 'joblist-comp-name').text.replace(' ','')
            skills = job.find('span',class_ = 'srp-skills').text.replace(' ','')
            more_info = job.header.h2.a['href']
            
            if unfamiliar_skill not in skills:
                cursor.execute("insert into fresher_job(company_name,skills,more_info) values(%s,%s,%s)",(company_name,skills,more_info))
                print(f'Company Name: {company_name.strip()}')
                print(f'Required Skills: {skills.strip()}')
                print(f'More Info: {more_info}')
                connect.commit()            

                print('')
find_jobs()
