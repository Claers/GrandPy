import pytest

import sys
sys.path.append("../")

from gmap import *

def test_create_map():
	map = Map("map","your_api_key")
	assert map.name == "map"




