import pytest
import json
import sys

sys.path.append("../")

from gmap import *

map = Map("map","your_api_key")

def test_create_map():
	assert map.name == "map"

def test_map_server_response():
	response = map.getLocation("Réunion")
	assert response["status"] == "OK"
	assert response['results'][0]['address_components'][0]['long_name'] == "Réunion"



