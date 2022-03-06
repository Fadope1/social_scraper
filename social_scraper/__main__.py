"""
This will be invoked by python -m social_scraper.
Todo:
- Arg parser for a cli interface?

Currently only for direct testing
"""

import datetime
import logging
from social_scraper.scrapers import TwitterScraper
logging.basicConfig(level=logging.CRITICAL)

twitter_data = TwitterScraper(debug=False) # debug: no actuall request will be made
twitter_data.get_tweets(
    hashtags=["BASF", "Ludwigshafen"], # search tweets with hastag
    # hashtags_recursive=True, # research with newly found hastags from content scrape
    # usernames=["elon musk", "bill gates"], # search user last tweets
    # searchbar=("stock", "stocks"), # search like twitter searchbar
    # list_search=["username/listname"],
    # ids=["idOfTweet"],
    # id_recursive=True, # id_search with comments etc. (maybe slow)
    since=datetime.datetime.today()-datetime.timedelta(days=0),
    # until=datetime.datetime.today()+datetime.timedelta(days=1),
    filter=("links", "replies"),
    max_results=100
)

import pandas as pd

data = pd.DataFrame(twitter_data.data)

print("dataframe.", data)

data.to_csv("out.csv")

# print(twitter_data + twitter_data)
# print(twitter_data + twitter_data + twitter_data)
