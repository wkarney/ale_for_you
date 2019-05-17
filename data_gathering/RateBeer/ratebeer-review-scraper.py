'''
Credit for tackling infinite scrolling goes to Stack Overflow user Cuong Tran 
https://stackoverflow.com/a/43299513/10919788

Note that this scraper runs rather sl
'''

import pandas as pd
from datetime import datetime
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument('headless')
driver = webdriver.Chrome(executable_path='../chromedriver',chrome_options=chrome_options)

beer_df = pd.read_csv('../../data/dmv_beerlinks.csv')

beer_link_list = beer_df.loc[:,'link'].values.tolist()
beer_name_list = beer_df.loc[:,'name'].values.tolist()

num_batches = 48
batch_size = len(beer_link_list) // num_batches

last_batch_additional = len(beer_link_list) % num_batches

for batch in range(num_batches):

    startpt = batch * batch_size

    if batch != (num_batches - 1):
        endpt = batch * batch_size + batch_size
    else:
        endpt = len(beer_link_list)

    all_reviews = []
    
    print(f"Running batch number {batch}: beer {startpt} to beer {endpt}")

    for num in range(startpt, endpt):

        driver.get(f'http://{beer_link_list[num]}')

        # Terminal output status check
        print(f"Pulling reviews of {beer_name_list[num]}")

        SCROLL_PAUSE_TIME = 2

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        count = 0
        while True and count < 5:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            count += 1

        sleep(2) 

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        
        user_soup = soup.find_all('a',{'class':'jss47 jss55 jss82 Anchor___StyledText-uWnSM itcYqU colorized__WrappedComponent-apsCh klBWXf Text___StyledTypography-eDaOFe kKzTmh'})
        users = [item['href'][6:-1] for item in user_soup if (item['_color'] == "#3f51b5") and ('(' in item.text)]
        
        rating_soup = soup.find_all('span',{'class':'jss47 jss55 jss82 text-500 ml-2 colorized__WrappedComponent-apsCh gsrvCV Text___StyledTypography-eDaOFe kKzTmh'})
        ratings = [item.text for item in rating_soup]

        review_soup = soup.find_all('div',{'class':'LinesEllipsis'})[1:]
        review_text = [item.text for item in review_soup]
                
        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        date_soup = soup.find_all('div',{'class':'jss47 jss57 colorized__WrappedComponent-apsCh jPmvJP Text___StyledTypography-eDaOFe kKzTmh'})
        dates = [datetime.strptime(date.text, '%b %d, %Y') for date in date_soup if date.text[:3] in months]
        
        beer_reviews = []

        review_list_size = min(len(dates), len(review_text), len(ratings), len(users))
        # Terminal status checks
        print(f"Date list size: {len(dates)}")
        print(f"User list size: {len(users)}")
        print(f"Rating list size: {len(ratings)}")
        print(f"Review list size: {len(review_text)}")
        print(f"Agg list size: {review_list_size}")
        
        for i in range(review_list_size):
            this_review = {}
            this_review['user'] = users[i]
            this_review['rating'] = ratings[i]
            this_review['review_text'] = review_text[i]
            this_review['date'] = dates[i]
            this_review['beer'] = beer_name_list[num]

            beer_reviews.append(this_review)
        
        all_reviews.extend(beer_reviews)

    brewreviews = pd.DataFrame(all_reviews, columns=['beer','user', 'date', 'rating', 'review_text'])

    brewreviews.to_csv(f'../scrape_output/review_batching/dmv_beer_review_text_batch{batch}.csv',index=False)

driver.close()