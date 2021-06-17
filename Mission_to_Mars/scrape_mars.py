from splinter import Browser
from bs4 import BeautifulSoup
import requests
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo
import time


def scrape():

    ## NASA Mars News
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    listings = {}

    # URL of page to be scraped
    url = 'https://redplanetscience.com'  

    # Retrieve page with the requests module
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")


    news_title = soup.find_all('div', class_='content_title')[0].text
    news_paragraph = soup.find_all('div', class_='article_teaser_body')[0].text

    ## JPL Mars Space Images - Featured Image

    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('img', class_='headerimage fade-in')

    for result in results:
        print(result['src'])
        img_url=result['src']

    featured_image_url= url +"/"+ img_url

    ### Mars Facts

    url="https://galaxyfacts-mars.com"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    tables = pd.read_html(url)
    df = tables[0]
    
    df=df.to_html(index=False, header=0)

    ### Mars Hemispheres

    url="https://marshemispheres.com/"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    
    soup = BeautifulSoup(html, 'html.parser')

    url1="https://marshemispheres.com/images/full.jpg"
    url2="https://marshemispheres.com/images/schiaparelli_enhanced-full.jpg"
    url3="https://marshemispheres.com/images/syrtis_major_enhanced-full.jpg"
    url4="https://marshemispheres.com/images/valles_marineris_enhanced-full.jpg"
    urls=[url1,url2,url3,url4]

    results = soup.find_all('div', class_='description')
    title_list=[]
    for result in results:
        title=result.find('h3').text
        title_list.append(title)


    my_dic={}
    my_list=[]
    x=range(0,4)
    for i in x: 
            my_dic['title']=title_list[i]
            my_dic['urls']=urls[i]
            my_list.append(my_dic.copy())
    
    
    # dic=[{"title":"Cerberus Hemisphere Enhanced","img_url":"https://marshemispheres.com/images/full.jpg"},
    #     {"title":"Schiaparelli Hemisphere Enhanced","img_url":"https://marshemispheres.com/images/schiaparelli_enhanced-full.jpg"},
    #     {"title":"Syrtis Major Hemisphere Enhanced","img_url":"https://marshemispheres.com/images/syrtis_major_enhanced-full.jpg"},
    #     {"title":"Valles Marineris Hemisphere Enhanced","img_url":"https://marshemispheres.com/images/valles_marineris_enhanced-full.jpg"}]


    listings["news_title"] = news_title
    listings["news_paragraph"] = news_paragraph
    listings["featured_image_url"] = featured_image_url
    listings["table"] = df
    listings["hemisphere"] = my_list




    # Quit the browser
    browser.quit()

    return listings




