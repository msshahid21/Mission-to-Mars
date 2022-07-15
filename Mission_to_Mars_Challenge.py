#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import selenium

import pandas as pd


# In[3]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless = False)


# ### Article Scraping

# In[52]:


# Visit the mars NASA news Site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[53]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')


# In[54]:


news_text = slide_elem.find('div', class_='content_title').get_text()
news_text


# In[55]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[56]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[57]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[58]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[59]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')


# In[60]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[61]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns = ['description', 'Mards', 'Earth']
df.set_index('description', inplace = True)
df


# In[62]:


df.to_html()


# In[63]:


browser.quit()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[38]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[39]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemisphere_soup = soup(html, 'html.parser')

hemispheres = hemisphere_soup.find_all('a', class_='itemLink product-item')
titles = hemisphere_soup.find_all('h3')[:-1]

for i in range(len(titles)):
    title = titles[i].text

    browser.links.find_by_partial_text(title).click()
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')

    hemisphere = browser.links.find_by_partial_text('Sample')[0]['href']
    hemisphere_image_urls.append({'img_url': hemisphere, 'title': title})

    browser.back()


# In[40]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[31]:


# 5. Quit the browser
browser.quit()

