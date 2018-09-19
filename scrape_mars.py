# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import tweepy
import json
from config import consumer_key, consumer_secret, access_token, access_token_secret
import pandas as pd
import pymongo

# Initialize browser
def init_browser():

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Function to scrape websites for Mars info
def scrape():

    # Create dictionary to store info about Mars
    mars_info = {}

    # Initialize browser
    browser = init_browser()

    # Using Splinter to visit website
    # Using BeautifulSoup to parse HTML
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Scraping website for latest news title
    news_title = soup.find("div", class_="content_title").text

    # Scraping website for latest news text
    news_p = soup.find("div", class_= "article_teaser_body").text

    # Adding info into dictionary
    mars_info["news_title"] = news_title
    mars_info["news_p"] = news_p

    # Using Splinter to visit website
    # Using BeautifulSoup to parse HTML
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Scraping website for featured image title
    image_title = soup.find("h1", class_="media_feature_title").text.strip()

    # Scraping website for featured image url
    image_url = soup.find("article")
    image_url = image_url['style'].split("'")[1]

    # Split url for base url
    split_url = urlsplit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    # Combining base url and featured image url for full url
    featured_image_url = split_url.scheme + "://" + split_url.netloc + image_url

    # Adding info into dictionary
    mars_info["image_title"] = image_title
    mars_info["featured_image_url"] = featured_image_url

    # Setup Tweepy API Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    # Target User
    target_user = "MarsWxReport"

    # Retrieving the latest tweet
    public_tweets = api.user_timeline(target_user, count=1)

    # Extracting only the "text" from the Tweet
    mars_weather = public_tweets[0]["text"]

    # Adding info into dictionary
    mars_info["mars_weather"] = mars_weather

    # Using Pandas to scrape data from tables
    # Note: There is only 1 table on this site 
    mars_facts_url = "http://space-facts.com/mars/"
    mars_facts = pd.read_html(mars_facts_url)

    # Since the info scraped from the website is a list, 
    # We need to turn it into a DataFrame
    # And give the column descriptive names 
    mars_df = mars_facts[0]
    mars_df.columns = ["Description", "Values"]

    # Converting DataFrame to HTML table string 
    # And Removing "\n"
    mars_html = pd.DataFrame.to_html(mars_df)
    mars_html = mars_html.replace("\n", "")

    # Adding info to dictionary
    mars_info["mars_df"] = mars_df
    mars_info["mars_html"] = mars_html

    # Getting the base url from main website
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    split_hemi_url = urlsplit(hemisphere_url)
    base_hemi_url = split_hemi_url.scheme + "://" + split_hemi_url.netloc

    # Creating a list to store info
    hemisphere_image_urls = []

    # Visiting website using Splinter
    hemisphere_url_1 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    browser.visit(hemisphere_url_1)

    # Using BeautifulSoup to parse HTML
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Getting the title of the specific hemisphere
    hemi_title_1 = soup.find("h2", class_="title").text
    hemi_title_1 = hemi_title_1.replace(" Enhanced", "")

    # Retrieving url for full resolution image
    hemi_1 = soup.find("img", class_="wide-image")
    hemi_1 = hemi_1["src"]

    # Adding base url to image url
    hemi_url_1 = base_hemi_url + hemi_1

    # Saving info to a dictionary and appending to a list
    cerberus = {"title": hemi_title_1, "img_url": hemi_url_1}
    hemisphere_image_urls.append(cerberus)

    # Visiting website using Splinter
    hemisphere_url_2 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    browser.visit(hemisphere_url_2)

    # Using BeautifulSoup to parse HTML
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Getting the title of the specific hemisphere
    hemi_title_2 = soup.find("h2", class_="title").text
    hemi_title_2 = hemi_title_2.replace(" Enhanced", "")

    # Retrieving url for full resolution image
    hemi_2 = soup.find("img", class_="wide-image")
    hemi_2 = hemi_2["src"]

    # Adding base url to image url
    hemi_url_2 = base_hemi_url + hemi_2

    # Saving info to a dictionary and appending to a list
    schiaparelli = {"title": hemi_title_2, "img_url": hemi_url_2}
    hemisphere_image_urls.append(schiaparelli)

    # Visiting website using Splinter
    hemisphere_url_3 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    browser.visit(hemisphere_url_3)

    # Using BeautifulSoup to parse HTML
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Getting the title of the specific hemisphere
    hemi_title_3 = soup.find("h2", class_="title").text
    hemi_title_3 = hemi_title_3.replace(" Enhanced", "")

    # Retrieving url for full resolution image
    hemi_3 = soup.find("img", class_="wide-image")
    hemi_3 = hemi_3["src"]

    # Adding base url to image url
    hemi_url_3 = base_hemi_url + hemi_3

    # Saving info to a dictionary and appending to a list
    syrtis_major = {"title": hemi_title_3, "img_url": hemi_url_3}
    hemisphere_image_urls.append(syrtis_major)

    # Visiting website using Splinter
    hemisphere_url_4 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    browser.visit(hemisphere_url_4)

    # Using BeautifulSoup to parse HTML
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Getting the title of the specific hemisphere
    hemi_title_4 = soup.find("h2", class_="title").text
    hemi_title_4 = hemi_title_4.replace(" Enhanced", "")

    # Retrieving url for full resolution image
    hemi_4 = soup.find("img", class_="wide-image")
    hemi_4 = hemi_4["src"]                             

    # Adding base url to image url
    hemi_url_4 = base_hemi_url + hemi_4

    # Saving info to a dictionary and appending to a list
    valles_marineris = {"title": hemi_title_4, "img_url": hemi_url_4}
    hemisphere_image_urls.append(valles_marineris)

    mars_info["hemisphere_image_urls"] = hemisphere_image_urls 

    return mars_info