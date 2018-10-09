import pytest
import sys

sys.path.append("../")

from grandpy.strparser import parser

def test_parser():
	response = parser("Salut ! Tu connais la rue de paris à la réunion ?")
	assert response == "rue paris réunion"