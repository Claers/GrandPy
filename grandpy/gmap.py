from urllib import parse
import requests

class Map:

	def __init__(self,name,api_key):
		self.name = name
		self.key = api_key

	# Get a location with name
	def getLocation(self,locationName):
		try:
			self.url = parse.urljoin(parse.urljoin("https://maps.googleapis.com/maps/api/", "place/queryautocomplete/"), "json") # Get a place Id for the location
			raw_response = requests.get(self.url,params = dict(key=self.key,input=locationName,inputtype="textquery"))
			response = raw_response.json()
			if(response['status'] == "ZERO_RESULTS"):
				return "Nothing"
			elif(response['status'] == "REQUEST_DENIED"):
				return "AccessDenied"
			else:
				locationId = response['predictions'][0]['place_id']
				self.url = parse.urljoin(parse.urljoin("https://maps.googleapis.com/maps/api/", "place/details/"), "json") # Get the details for the place id
				raw_response = requests.get(self.url,params = dict(key=self.key,placeid=locationId,inputtype="textquery",fields="formatted_address,name,geometry"))
				response = raw_response.json()
				if(response['status'] == "ZERO_RESULTS"):
					return "Nothing"
				elif(response['status'] == "REQUEST_DENIED"):
					return "AccessDenied"
				else:
					return response
		except:
			return "InternalError"
			pass


