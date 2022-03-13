"""
This class is for retreiving posts/ tweets etc. from social media sites, with simple inputs.

TODO:
- logging
"""

from typing import Tuple, List, Union
import datetime
import logging

from attrs import define

from social_scraper.exceptions import MaxCountReached, InvalidInput

# CONSTANTS:
DEFAULT_VAR_VALUE = None # default value for not set args

DATETIME_OBJECTS = (datetime.datetime, datetime.date) # all accepted date objects
ITERABLE_OBJECTS = (list, tuple)

# allowed args and types for parsers
QUERY_KWARGS: dict = {
    "since": DATETIME_OBJECTS,
    "until": DATETIME_OBJECTS,
    "filter": ITERABLE_OBJECTS, # list[str], tuple[str]
}

QUERY_NAMESPACE: dict = {
    "filter": "-fitler"
}

QUERY_KEYS: tuple = tuple((key for key in QUERY_KWARGS)) # get keys of QUERY_KEYS
QUERY_ARG_TYPES: tuple = ()
for _, value in QUERY_KWARGS.items():
    QUERY_ARG_TYPES += value

OPTIONAL_KWARGS: Tuple[str] = ("max_results",)
REQUIRED_KWARGS: Tuple[str] = ()
KWARGS_TYPES: tuple = (int, bool) + QUERY_ARG_TYPES


# TODO: Namedtuple better?
# TODO: Learn slots -> Usecase?
@define(frozen=True)
class Post:
    """Stores the data received from snscrape."""
    date: DATETIME_OBJECTS
    id: str
    content: str
    username: str
    query: str


class SocialAnalyser:
    """
    Base class for all scrapers.
    Used to parse kwargs/ args and handle magical operations like addition of objects and
    characterizing/ analysing content.
    """

    def __init__(self, debug:bool = False, data: List[Post]=None) -> None:
        if data is None:
            data = [] # data initialized with empty list for __add__ operation

        self.data: List[Post] = data
        self.counter: int = 0 # data counter (count tweets/ posts etc.)

        # Defaults:
        self.debug: bool = debug # no requests will be made when set to True (default:False)
        self.var_names: list = []

    def parse_search_parameter(self, search_query) -> str:
        """This builds the search query."""
        query = f"{search_query} " # base search query

        for key, values in QUERY_KWARGS.items():

            var = self[key] # call __getitem__
            var_type = type(var)

            if var_type in values:
                # rename var for snscrape
                key = QUERY_NAMESPACE.get(key, key)

                if var_type in DATETIME_OBJECTS:
                    query += f"{key}:{var:%Y-%m-%d} "
                    continue

                if var_type in ITERABLE_OBJECTS:
                    for value in var:
                        query += f"{key}:{value} "
                    continue

                query += f"{key}:{var} "
            elif var is not DEFAULT_VAR_VALUE:
                raise TypeError(f"{var_type} is wrong type for keyword = {key}")

        logging.debug("Searching for: %s", query)

        return query

    def scraper(self, search_method: type, query: str) -> Union[None, str]:
        """This runs the given scraper using the query."""
        search_query: str = self.parse_search_parameter(query)

        if self.debug:
            return

        search_result = search_method(search_query).get_items()

        for post in search_result:
            # stop if max_results reached if not None (no limit)
            if self.max_results != DEFAULT_VAR_VALUE and self.counter >= self.max_results:
                raise MaxCountReached(f"Max count of tweets encountered at count {self.counter}")

            # construct the post
            post = Post(
                        date=post.date,
                        id=post.id,
                        content=post.content,
                        username=post.username,
                        query=search_query
                    )

            # append if not already in data
            if post not in self.data:
                self.data.append(post)

            self.counter += 1 # increase request tweet counter

            yield post.content

    def parse_kwargs(self, kwargs) -> None:
        """Parse keyword args to self -> run corresponding methods with args."""
        scraper_vars: tuple = self.var_names + OPTIONAL_KWARGS + REQUIRED_KWARGS + QUERY_KEYS # all keywords

        # check the validity of kwargs
        if not self.__is_valid(kwargs, scraper_vars):
            raise InvalidInput("To much arguments supplied.")

        unset_vars: dict = {key: DEFAULT_VAR_VALUE for key in scraper_vars} # set all vars as unset

        # set vars to self
        for key in scraper_vars:
            if key in kwargs:
                # not in accepted type list
                if type(kwargs[key]) not in KWARGS_TYPES:
                    raise TypeError(f"Wrong type for '{key}' with type = '{type(kwargs[key])}'")
                setattr(self, key, kwargs[key])
                del unset_vars[key] # delete var from unset dict (mark as set)
                del kwargs[key] # delete key from kwargs

        # set unset vars to ""
        for unset_key, value in unset_vars.items():
            if unset_key in REQUIRED_KWARGS:
                raise InvalidInput(f"Required arg {unset_key} missing")
            setattr(self, unset_key, value)

        # start the corresponding methods from the subclass with parameters
        assert len(kwargs.items()) > 0, "No function calls provided"
        for key, value in kwargs.items():
            if type(value) not in (list, tuple):
                raise TypeError(f"{key} has to be supplied with type list or tuple, not type = {type(value)}")

            try:
                exec(f"self.{key}_search({value})") # run corresponding method from child class
            except MaxCountReached as err:
                # if max count was reached stop the scraping process
                logging.debug(err)
                break

    def get_posts(self, **kwargs) -> None:
        """User function. Overwritten by some scrapers."""
        self.parse_kwargs(kwargs)

    def add_variables(self, *var_names: str) -> None:
        """This registers the custom variables as valid."""
        # TODO: perform var_names check here -> no duplicates etc.
        self.var_names = var_names

    def __is_valid(self, kwargs, scraper_vars: tuple) -> bool:
        """Check if all kwargs are either a known function or a variable argument."""
        return all(((f"{key}_search" in dir(self) or key in scraper_vars) for key in kwargs))

    def __add__(self, other: type) -> type:
        """Adds 2 scrapers data together (scraper1.data + scraper2.data)."""
        temp = self.data[::].extend(other.data)
        return SocialAnalyser(debug=self.debug, data=temp)

    def __getitem__(self, key: str):
        """Get attribute by str name, called with self[key]"""
        return getattr(self, key)
