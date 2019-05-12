from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome(executable_path='../chromedriver')

# regionalurl = input("Please enter the full url for your region: ")
# region_name = input("Please enter the region name: ")

arealist =[
    {
    'url':'https://www.ratebeer.com/breweries/maryland/20/213/',
    'name': 'MD'
    }]

for state in arealist:
    driver.get(state['url'])

    sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    table = soup.find('table',{'id':'brewerTable'})

    region_brews = []

    for i in range(len(table.find_all('a'))):
        brewery = {}
        if i % 2 == 0:
            brewery['name'] = table.find_all('a')[i].text
            brewery['link'] = f"http://www.ratebeer.com{table.find_all('a')[i]['href']}"
        else:
            continue
        region_brews.append(brewery)

    allbrews = []

    for brewery in region_brews:
        
        driver.get(brewery['link'])
        sleep(10)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        
        table = soup.find('table',{'id':'brewer-beer-table'})
        
        beermenu = []
        try:
            table.find('tbody').find_all('tr')
        except:
            try:
                newlink = f"http://www.ratebeer.com{soup.find_all('em')[-1].find('a')['href']}"
                driver.get(newlink)
                sleep(10)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
        
                table = soup.find('table',{'id':'brewer-beer-table'})
            except:
                continue
            
        for row in table.find('tbody').find_all('tr'):
            beer = {}
            beer['brewery'] = brewery['name']
            beer['name'] = row.find('a').text
            beer['style'] = row.find('span').text
            beer['link'] = f"www.ratebeer.com{row.find('a')['href']}"
            try:
                beer['style_rating'] = float(row.find_all('td')[-2].text)
            except:
                beer['style_rating'] = None
            try:
                beer['abv'] = round(float(row.find('td',{'class':'hidden-xs'}).text)/100,3)
            except:
                beer['abv'] = None
            try:
                beer['date_added'] = row.find_all('td',{'class':'text-left'})[0].text
            except:
                beer['date_added'] = None
            try:
                beer['rating'] = float(row.find_all('td')[-3].text)
            except:
                beer['rating'] = None
            try:
                beer['num_ratings'] = int(row.find_all('td',{'class':'text-left'})[-1].text)
            except:        
                beer['num_ratings'] = 0

            beermenu.append(beer)

        allbrews.extend(beermenu)

    brewlist = pd.DataFrame(allbrews)

    brewlist.to_csv(f'./data/brewlist_{state["name"]}.csv',index=False)

driver.close()