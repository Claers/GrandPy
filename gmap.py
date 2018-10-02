from urllib import parse
import requests

class Map:

	def __init__(self,name,api_key):
		self.name = name
		self.key = api_key

	def getLocation(self,locationName):
		self.url = parse.urljoin(parse.urljoin("https://maps.googleapis.com/maps/api/", "geocode/"), "json")
		raw_respone = requests.get(self.url,params = dict(key=self.key,address=locationName))
		response = raw_respone.json()
		return response

