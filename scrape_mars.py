from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tag_articles = soup.find_all('div', class_='article_teaser_body')
    list_article = []
    for each in tag_articles:
        list_article.append(each.text)

    tag_titles = soup.find_all('div', class_='content_title')
    list_title = []

    for each in tag_titles[0:41]:
        if each.a:
            list_title.append(each.a.extract().text.strip('\n'))

    news_title = list_title[0]
    news_article = list_article[0]
    browser.quit()
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(3)

    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')
    list_urltags =soup2.find_all('a', class_='fancybox', id=False)
    list_url = []
    for each in list_urltags:
        list_url.append("https://www.jpl.nasa.gov" + str(each['data-fancybox-href']))
        
    featured_image_url = list_url[0]

    url = "https://space-facts.com/mars/"

    tables = pd.read_html(url)
    mars_df = tables[1].iloc[:,0:2]
    mars_df.columns = ["Category","Data"]
    mars_df.set_index('Category', inplace=True)
    mars_df.to_html("mars_data.html")
    table_mars = mars_df.to_html()
    mars_table = table_mars.replace('\n', '')
    browser.quit()
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    info_tags = soup.find_all("div",class_="item")
    hemisphere_image_urls = []
    for tag in info_tags:
        hemisphere_image_urls.append({"title":tag.h3.text,"img_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/" + tag.a["href"].split("/")[5] + ".tif/full.jpg"})


    browser.quit()


    scraped_data = {"news_title":news_title,"news_article":news_article,"featured_image_url":featured_image_url,"mars_table":mars_table,"hemisphere_image_urls":hemisphere_image_urls}
    return scraped_data

