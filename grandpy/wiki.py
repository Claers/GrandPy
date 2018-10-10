from urllib import parse
from urllib.parse import unquote
from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import random
import re


class Wiki:

    def __init__(self, name):
        self.name = name
        self.articles = {}

    # Find a article with coordinates
    def getArticleWithLocation(self, location, locRange):
        print(location)
        self.url = "https://fr.wikipedia.org/w/api.php?action=query&format=json&prop=pageterms%7Cinfo&list=&meta=&generator=geosearch&wbptcontinue=&wbptterms=description&inprop=url&ggscoord=" + \
            str(location['lat']) + "|" + str(location['lng']) + \
            "&ggsradius=" + locRange + "&ggslimit=10"
        raw_response = requests.get(self.url)
        if(isinstance(raw_response, requests.models.Response)):  # Used for the tests
            response = raw_response.json()
            return response
        else:
            return raw_response

        # Find a article with name
    def getArticleWithName(self, name):
        self.url = "https://fr.wikipedia.org/w/api.php?action=opensearch&search=" + name
        raw_response = requests.get(self.url)
        response = raw_response.json()
        if(isinstance(raw_response, requests.models.Response)):  # Used for the tests
            if(response[1] == []):
                return None
            else:
                return response
        else:
            return raw_response

    # Get the first line of the first paragraph of an article
    def getArticleParagraph(self, articleUrl):
        self.url = articleUrl
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # Usually the first paragraph is after the first h2
        p = soup.find("h2").findNext('p')
        if(p != None):
            goodh = p.get_text().strip()
            regex = re.compile(".*?\([.*?]\)")
            result = re.sub("[\[].*?[\]]", "", goodh)
            return result
        else:
            return "InternalError"
