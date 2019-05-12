from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome(executable_path='../chromedriver')

# regionalurl = input("Please enter the full url for your region: ")
# region_name = input("Please enter the region name: ")

arealist =[
    {
    'url':'https://www.ratebeer.com/breweries/washington-dc/48/213/',
    'name': 'DC'
    },
    {
    'url':'https://www.ratebeer.com/breweries/delaware/8/213/',
    'name': 'DE'
    },
    {
    'url':'https://www.ratebeer.com/breweries/maryland/20/213/',
    'name': 'MD'
    },
    {
    'url':'https://www.ratebeer.com/breweries/pennsylvania/38/213/,
    'name': 'PA'
    },
    {
    'url':'https://www.ratebeer.com/breweries/virginia/46/213/',
    'name': 'VA'
    },
    {
    'url':'https://www.ratebeer.com/breweries/west%20virginia/49/213/',
    'name': 'WV'
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

    for brewery in region_brews[:1]:
        
        driver.get(brewery['link'])
        sleep(10)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        
        try:
            brewery['google_map_link'] = soup.find('a',{'title':'View beermap'})['href'][2:]
        except:
            brewery['google_map_link'] = None
        try:
            brewery['address'] = soup.find('a',{'title':'View beermap'}).find_all('span')[0].text
        except:
            brewery['address'] = None
        try:
            brewery['town'] = soup.find('a',{'title':'View beermap'}).find_all('span')[1].text
        except:
            brewery['town'] = None
        try:
            brewery['state'] = soup.find('a',{'title':'View beermap'}).find_all('span')[2].text
        except:
            brewery['state'] = None
        try:
            brewery['country'] = soup.find('a',{'title':'View beermap'}).find_all('span')[3].text
        except:
            brewery['country'] = None
        try:
            brewery['postal_code'] = soup.find('a',{'title':'View beermap'}).find_all('span')[4].text
        except:
            brewery['postal_code'] = None

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
            beer['name'] = row.find('a').text
            beer['style'] = row.find('span').text
            beer['link'] = f"www.ratebeer.com{row.find('a')['href']}"
            beer['brewery'] = brewery['name']
            beer['google_map_link'] = brewery['google_map_link']
            beer['address'] = brewery['address']
            beer['town'] = brewery['town']
            beer['state'] = brewery['state']
            beer['country'] = brewery['country']
            beer['postal_code'] = brewery['postal_code']
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

    brewlist.to_csv(f'../../data/brewlist_{state["name"]}.csv',index=False)

driver.close()