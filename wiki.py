from urllib import parse
import requests

class Wiki:

	def __init__(self,name):
		self.name = name

	def getArticleUrl(self,articleName):
		self.url = "https://fr.wikipedia.org/w/api.php?action=opensearch&format=json&search=" + articleName
		raw_respone = requests.get(self.url)
		response = raw_respone.json()
		return response[3][0]

	def getArticleDesc(self,articleName):
		self.url = "https://fr.wikipedia.org/w/api.php?action=opensearch&format=json&search=" + articleName
		raw_respone = requests.get(self.url)
		response = raw_respone.json()
		return response[2][0]