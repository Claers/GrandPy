from urllib import parse
from urllib.parse import unquote
from bs4 import BeautifulSoup,NavigableString, Tag
import requests
import random
import re

class Wiki:

	def __init__(self,name):
		self.name = name
		self.articles = {}

	def getArticleWithLocation(self,location,locRange):
		print(location)
		self.url = "https://fr.wikipedia.org/w/api.php?action=query&format=json&prop=pageterms%7Cinfo&list=&meta=&generator=geosearch&wbptcontinue=&wbptterms=description&inprop=url&ggscoord=" + str(location['lat']) + "|" + str(location['lng']) + "&ggsradius="+locRange+"&ggslimit=10" 
		raw_response = requests.get(self.url)
		if(isinstance(raw_response, requests.models.Response)):
			response = raw_response.json()
			return response
		else:
			return raw_response

	def getArticleWithName(self,name):
		self.url = "https://fr.wikipedia.org/w/api.php?action=opensearch&search=" + name
		raw_response = requests.get(self.url)
		response = raw_response.json()
		if(isinstance(raw_response, requests.models.Response)):
			if(response[1] == []):
				return None
			else:
				return response
		else:
			return raw_response
		

	def getArticleParagraph(self,articleUrl):
		self.url = articleUrl
		page = requests.get(self.url)
		soup = BeautifulSoup(page.content,'html.parser')
		p = soup.find("h2").findNext('p')
		if(p != None):
			goodh = p.get_text().strip()
			regex = re.compile(".*?\([.*?]\)")
			result = re.sub("[\[].*?[\]]", "" ,goodh)
			return result
		else:
			return "InternalError"
			