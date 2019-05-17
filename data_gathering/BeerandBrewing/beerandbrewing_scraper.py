import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from time import sleep

driver = webdriver.Chrome(executable_path='../chromedriver')

allreviews = pd.DataFrame()

for pg in range(34):
    url = f'https://beerandbrewing.com/beer-reviews/?q=&hPP=30&idx=cbb_web_review_search&p={pg}'
    driver.get(url)
    sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    
    desc = soup.find_all('p',{'class':"hit-description"})
    reviews = []
    for brew in desc:
        beer = {}
        beer['description'] = brew.text
        reviews.append(beer)
    
    reviews = pd.DataFrame(reviews)
    
    beersoup = soup.find_all('div', {'class':['hit-content', 'col-xs-12', 'col-sm-12', 'col-md-10', 'text-wrapper']})
    
    names = []
    links = []
    for i in beersoup[6:]:
        if i.find('img',{'alt':True}) != None:
            img = i.find('img',{'alt':True})
            names.append(img['alt'])
        if i.find('a',{'href':True}) != None:
            link =  i.find('a',{'href':True})
            links.append(link['href'])
    
    beerlinks = []
    for i in range(0, len(links)):
        if i % 2 == 0 and (links[i].find('review') == True) and (links[i] not in beerlinks):
            beerlinks.append(links[i])
    
    reviews['names'] = names
    reviews['links'] = beerlinks
    allreviews = allreviews.append(reviews)

beerandbrewing = allreviews.reset_index().drop(columns='index')
beerandbrewing.to_csv('../scrape_output/beerandbrewing_reviews.csv', index=False)

driver.close()