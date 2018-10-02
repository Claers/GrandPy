from urllib import parse
from urllib.parse import unquote
from bs4 import BeautifulSoup,NavigableString, Tag
import requests

class Wiki:

	def __init__(self,name):
		self.name = name

	def getArticleUrl(self,articleName):
		self.url = "https://fr.wikipedia.org/w/api.php?action=opensearch&format=json&search=" + articleName
		raw_response = requests.get(self.url)
		response = raw_response.json()
		if(response[1] == []):
			return None
		else:
			return unquote(response[3][0])

	def getArticleDesc(self,articleName):
		self.url = "https://fr.wikipedia.org/w/api.php?action=opensearch&format=json&search=" + articleName
		raw_response = requests.get(self.url)
		response = raw_response.json()
		if(response[1] == []):
			return None
		else:
			return unquote(response[2][0])

	def getArticleParagraph(self,articleUrl):
		self.url = articleUrl
		page = requests.get(self.url)
		soup = BeautifulSoup(page.content,'html.parser')
		body = soup('body')[0]
		goodh = soup.findAll('p')[4].get_text().strip()
		return goodh
		