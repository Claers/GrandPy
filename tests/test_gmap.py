import pytest

import sys
sys.path.append("../")

from gmap import *

map = Map("map","your_api_key")

def test_create_map():
	assert map.name == "map"

def test_map_server_response():
	response = map.getLocation("Reunion")
	assert response["status"] == "OK"



