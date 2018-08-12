
# coding: utf-8

# In[13]:


# Import BeautifulSoup for parsing and splinter for site navigation
import pandas as pd 
import time 
from bs4 import BeautifulSoup
from splinter import Browser
def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars = {}


    # In[14]:


    # Visit the NASA news URL
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)


    # In[15]:


    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # In[16]:


    # save the most recent article, title and date save  
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text

    mars["news_title"] = news_title
    mars["news_paragraph"] = news_p
    mars["news_date"] = news_date


    # In[17]:


    # Visit the JPL Mars URL
    url = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)


    # Scrape the browser into soup and use soup to find the image of mars
    # Save the image url to a variable called `img_url`
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find("img", class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url
    mars["featured_image"] = featured_image_url
    # Use the requests library to download and save the image from the `img_url` above
    #import requests
    #import shutil
    '''
    response = requests.get(img_url, stream=True)
    with open('img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
        
    # Display the image with IPython.display
    #from IPython.display import Image
    #Image(url='img.jpg')
    '''

    # In[25]:


    # Visit the Mars Weather twitter account and scrape the latest Mars weather tweet.
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
 




    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')



    mars_weather_tweet = weather_soup.find("div", attrs = {"class":"tweet", "data-name": "Mars Weather"})


    mars_recent_tweet = mars_weather_tweet.find("p", class_ = "tweet-text").get_text()

    mars["weather_info"] = mars_recent_tweet




    # Visit the Mars facts webpage and scrape table data into Pandas# Visit 
    url = "http://space-facts.com/mars/"
    browser.visit(url)
 






    # place data into a dataframe, clean it up and output it into an HTML table
    grab=pd.read_html(url)
    mars_data=pd.DataFrame(grab[0])
    mars_data.columns=['Mars','Data']
    mars_table=mars_data.set_index("Mars")
    marsdata = mars_table.to_html(classes='marsdata')
    marsdata=marsdata.replace('\n', ' ')
    mars["facts"] = marsdata


    # Visit the USGS Astogeology site and scrape pictures of the hemispheres
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(2)



    # In[32]:


    # Use splinter to loop through the 4 images and load them into a dictionary 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_hemis=[]


    # In[33]:


    # loop through the four tags and load the data to the dictionary

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()

    mars["hemispheres"] = mars_hemis

    return mars