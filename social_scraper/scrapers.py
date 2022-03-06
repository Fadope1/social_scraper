"""
Here are all scrapers classes for the Social Media sites.
"""

from typing import Union, List, Tuple
from snscrape import modules

from social_scraper.base import SocialAnalyser

ArgType = Union[List[str], Tuple[str]] # Either a list or tuple of strings


class TwitterScraper(SocialAnalyser):
    """Scraper for searching Twitter tweets"""

    def __init__(self, debug=False):
        super().__init__(debug=debug)
        self.add_variables("hashtags_recursive", "id_recursive")

    def scrape(self, search_method: None, query_terms: ArgType) -> None:
        """Helper method to iterate over all search_terms and run the scraper."""
        for term in query_terms:
            self.scraper(search_method=search_method, query=term)

    def hashtags_search(self, hashtags: ArgType) -> None:
        """Search twitter by hashtags."""
        self.scrape(search_method=modules.twitter.TwitterHashtagScraper, query_terms=hashtags)

    def usernames_search(self, usernames: ArgType) -> None:
        """Search twitter by username."""
        self.scrape(search_method=modules.twitter.TwitterUsernameScraper, query_terms=usernames)

    def searchbar_search(self, search_terms: ArgType) -> None:
        """Search twitter by using the searchbar."""
        self.scrape(search_method=modules.twitter.TwitterSearchScraper, query_terms=search_terms)

    def lists_search(self, lists: ArgType) -> None:
        """Search twitter list."""
        self.scrape(search_method=modules.twitter.TwitterListScraper, query_terms=lists)

    def ids_search(self, ids: ArgType) -> None:
        """Seach specific tweet by ids."""
        raise NotImplementedError
        self.scrape(search_method=modules.twitter.TwitterIDScraper, query_terms=ids)
        # self.id_recursive

    def get_tweets(self, **kwargs) -> None:
        """Just a (rename) wrapper method that actually runs the method
        (class specific rename)."""
        self.get_posts(**kwargs)


class RedditScraper(SocialAnalyser):
    """Scraper to search Reddit posts"""

    def __init__(self, debug=False):
        super().__init__(debug=debug)
        self.var_names = () # class specific vars

    def get_posts(self, **kwargs):
        """This will get a post by reddits search bar"""
        raise NotImplementedError("Reddit is not yet implemented")
