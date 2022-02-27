from social_scraper.base import SocialAnalyser

from snscrape import modules


class TwitterScraper(SocialAnalyser):
    """Scraper for searching Twitter tweets"""

    def __init__(self, debug=False):
        super().__init__(debug=debug)
        self.add_variables("hashtags_recursive", "id_recursive")

    def analyse_tweet(self, tweet) -> None:
        raise NotImplementedError("cannot analyze tweets atm")

    def hashtags_search(self, hashtags) -> None:
        """Search twitter by hashtags"""
        raise NotImplementedError("hashtag_search is not implemented yet")

    def usernames_search(self, usernames) -> None:
        """Search twitter by username"""
        raise NotImplementedError("usernames_search is not implemented yet")

    def searchbar_search(self, search_terms) -> None:
        """Search twitter by using the searchbar"""
        for search_term in search_terms:
            self.scraper(search_method=modules.twitter.TwitterSearchScraper, query=search_term)

    def list_search(self, lists) -> None:
        """Search twitter list"""
        raise NotImplementedError("list_search is not implemented yet")

    def id_search(self, ids) -> None:
        """Seach specific tweet by ids"""
        raise NotImplementedError("id_search is not implemented yet")
         # self.id_recursive

    def get_tweets(self, **kwargs) -> None:
        """Just a wrapper method that actually runs the actuall method (class specific rename)"""
        self.get_posts(**kwargs)


class RedditScraper(SocialAnalyser):
    """Scraper to search Reddit posts"""

    def __init__(self, debug=False):
        super().__init__(debug=debug)
        self.var_names = () # class specific vars

    def get_posts(self, **kwargs):
        raise NotImplementedError("Reddit is not yet implemented")
