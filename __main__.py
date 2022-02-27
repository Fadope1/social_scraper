import datetime

from social_scraper.Scrapers import TwitterScraper

twitter_data = TwitterScraper(debug=False)
twitter_data.get_tweets(
    # hashtags=["stocks", "stock", "trading"], # search tweets with hastag
    # hashtags_recursive=True, # research with newly found hastags from content scrape
    # usernames=["elon musk", "bill gates"], # search user last tweets
    searchbar=("stocks", "stock"), # search like twitter searchbar
    # list_search=["username/listname"],
    # id_search=["idOfTweet"],
    # id_recursive=True, # id_search with comments etc. (maybe slow)
    since=datetime.datetime.today()-datetime.timedelta(days=5), # 5 days ago max
    # until=datetime.datetime.today()+datetime.timedelta(days=1),
    filter=("links", "replies"),
    max_results=5 # max 25 results/ 0 = endless
)

print(twitter_data.data)

# print(twitter_data + twitter_data)
# print(twitter_data + twitter_data + twitter_data)
