import pytest
import json
import sys
import requests
from io import BytesIO


sys.path.append("../")

from grandpy.wiki import *

wikiClient = Wiki("wikiclient")

def test_create_wiki():
	assert wikiClient.name == "wikiclient"

def test_get_article_with_location(monkeypatch):
	results = {
		'batchcomplete': '', 'query': {'pages': {'7508': {'pageid': 7508, 'ns': 0, 'title': 'La Réunion', 'index': 0, 'terms': {'description': ["département et région d'outre-mer français situé dans l'Océan indien"]}, 'contentmodel': 'wikitext', 'pagelanguage': 'fr', 'pagelanguagehtmlcode': 'fr', 'pagelanguagedir': 'ltr', 'touched': '2018-10-03T11:08:55Z', 'lastrevid': 152681604, 'length': 117457, 'fullurl': 'https://fr.wikipedia.org/wiki/La_R%C3%A9union', 'editurl': 'https://fr.wikipedia.org/w/index.php?title=La_R%C3%A9union&action=edit', 'canonicalurl': 'https://fr.wikipedia.org/wiki/La_R%C3%A9union'}}}
	}

	def mockreturn(request):
		return json.dumps(results)

	monkeypatch.setattr(requests, 'get', mockreturn)
	
	resp = wikiClient.getArticleWithLocation({'lat': -21.115141, 'lng': 55.53638400000001},"1000")
	resp = json.loads(resp)
	assert resp['query']['pages']['7508']['pageid'] == 7508

def test_get_article_with_name():
	response = wikiClient.getArticleWithName("France")
	assert response[1][0] == "France"

