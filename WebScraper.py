import requests
import os
from bs4 import BeautifulSoup
import time
from datetime import datetime as dt
import datetime
import json
import config

CA=os.path.dirname(os.path.realpath(__file__))+'/certs/CA.pem'
proxyDict = { 
  'http':config.proxy,
  'https':config.proxy
}

start_scrap_epoc=int((datetime.datetime.now() - datetime.timedelta(minutes = 60)).timestamp())

def main():
  pretty_print_jsonArray((googlenews('covid-19')))
  pretty_print_jsonArray((newsnow('covid-19')))

def pretty_print_jsonArray(newsList):
  print(json.dumps(newsList, indent=2))

def get(url):
  r = requests.get(url, verify=CA, proxies=proxyDict)
  html_soup = BeautifulSoup(r.text, 'html.parser')
  return html_soup  

def googlenews(search_terms):
  news_feed_list = []
  url = 'https://news.google.com/search?q='+search_terms
  html_soup = get(url)

  feeds = html_soup.find_all('div', class_ = 'xrnccd') 

  for feed in feeds:
    news_epoc_time=int( dt.strptime( feed.find('time', class_ = 'WW6dff uQIVzc Sksgp')['datetime'] ,'%Y-%m-%dT%H:%M:%SZ').timestamp() )
    uri = (feed.article.h3.a['href']).replace('.', 'https://news.google.com', 1)
    title = feed.article.h3.a.text
    publish_time = str( dt.strptime( feed.find('time', class_ = 'WW6dff uQIVzc Sksgp')['datetime'] ,'%Y-%m-%dT%H:%M:%SZ') )
    publisher = feed.find('div', class_ = 'SVJrMe').a.text
    source = 'GoogleNews'

    if ( news_epoc_time > start_scrap_epoc):
      feedDict = {}
      feedDict["title"] = title
      feedDict["uri"] = uri
      feedDict["publish_time"] = publish_time
      feedDict["publisher"] = publisher
      feedDict["source"] = source
      news_feed_list.append(feedDict)
  
  return news_feed_list    

def newsnow(search_terms):
  news_feed_list = []
  #url = 'https://www.newsnow.co.uk/h/Business+&+Finance/Banking?type=ln'
  url = 'https://www.newsnow.co.uk/h/?search='+search_terms+'&lang=en&searchheadlines=1'
  html_soup = get(url)

  container = html_soup.find('div', class_ = 'rs-newsbox js-newsbox js-newsbox-raw js-newsmain js-central_ln_wrap')
  feeds = container.find_all('div', class_ = 'hl__inner')

  for feed in feeds:
    link = feed.a['href']
    if link.startswith('http'):
      news_epoc_time=int(feed.find('span', class_ = 'time')['data-time'])
      if ( news_epoc_time > start_scrap_epoc):
        uri = feed.a['href']
        title = feed.a.text
        publish_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(  news_epoc_time    )  )
        publisher = feed.find('span', class_ = 'src-part').text
        source = 'NewsNow'
        feedDict = {}
        feedDict["title"] = title
        feedDict["uri"] = uri
        feedDict["publish_time"] = publish_time
        feedDict["publisher"] = publisher
        feedDict["source"] = source
        news_feed_list.append(feedDict)
  
  return news_feed_list

if __name__== "__main__":
  main()        