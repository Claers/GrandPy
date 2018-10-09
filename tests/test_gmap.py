import pytest
import json
import sys

sys.path.append("../")

from grandpy.gmap import *

map = Map("map","AIzaSyCiGYAXBI0xmj1SVqAVYDHUA-6ceTPXbT8")

def test_create_map():
	assert map.name == "map"

def test_map_server_response():
	response = map.getLocation("Réunion")
	assert response["status"] == "OK"
	assert response['result']['name'] == "Réunion"



