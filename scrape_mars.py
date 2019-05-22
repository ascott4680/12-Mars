import pandas as pd
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import os




def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)


def scrape_info():
    browser = init_browser()

    
    #URL of page to be scrapted
    url = 'https://mars.nasa.gov/news/'
    #browser visits the url
    browser.visit(url)

    #let the page load fully
    #time.sleep(1)


    #assign the variables
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #quit browser
    #browser.quit()

    #find article title--------------------------------------------------
    results = soup.find('div', class_='content_title')

    news_title = results.text.lstrip()

    #find body text of first article---------------------------------------
    results2 = soup.find('div', class_='article_teaser_body')

    news_p = results2.text.lstrip()

    #getting connection refused errors, sleeping 
    #time.sleep(1)


    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    #time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    image = soup.find('div', class_='default floating_text_area ms-layer')
    featured_image=image.find('footer')
    fi_url=featured_image.find('a')['data-fancybox-href']
    featured_image_url= 'https://www.jpl.nasa.gov'+ fi_url

    #browser.quit()
    
    #Sleeping again to be safe
    #time.sleep(1)


    # URL of page to be scraped
    twitter = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    t_response = requests.get(twitter)

    # Create BeautifulSoup object; parse with 'lxml'
    mars_soup = BeautifulSoup(t_response.text, 'lxml')


    #find article title--------------------------------------------------
    mars_tweet = mars_soup.find_all('div', class_='js-tweet-text-container')[0].text
    mars_tweet = mars_tweet.replace('\n','').split('pic.twitter')[0]



    table_url = 'https://space-facts.com/mars/'

    mars_facts = pd.read_html(table_url)

    df = mars_facts[0]
    df.columns = ['Measurement', 'Value']

    #Set index to Measurement Column
    df.set_index('Measurement', inplace=True)


    # Export to HTML
    mars_d_table = df.to_html()
    # html.replace("\n", "")
    # df.to_html('mars.html')


    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    #time.sleep(2)
    base='https://astrogeology.usgs.gov'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    images = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    for image in images:
        hemi_dict={}
        
        link= image.a['href']
        hemi_link=base+link
        hemisphere_image_urls.append(hemi_dict)
        browser.visit(hemi_link)
        
        #time.sleep(1)
        current_html=browser.html
        current_soup = BeautifulSoup(current_html, 'lxml')
        cs_find= current_soup.find('h2', class_='title')
        title=cs_find.text.lstrip()
        pic_url=current_soup.find('div', class_='downloads').find('a')['href']
        hemi_dict['title']=title    
        hemi_dict['img_url']=pic_url

        

    browser.quit()

    # Store data in a dictionary
    mars_data = {
        "news_header": news_title,
        "news_body": news_p,
        "featured_image": featured_image_url,
        "tweet": mars_tweet,
        "table": mars_d_table,
        "hemisphere": hemisphere_image_urls
    }

   
    # Return results
    return mars_data
