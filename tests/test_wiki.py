import pytest
import json
import sys

sys.path.append("../")

from wiki import *

wikiClient = Wiki("wikiclient")

def test_create_wiki():
	assert wikiClient.name == "wikiclient"

def test_get_article_Url():
	response = wikiClient.getArticleUrl("France")
	assert response == "https://fr.wikipedia.org/wiki/France"

def test_get_article_Desc():
	response = wikiClient.getArticleDesc("France")
	assert response == "La France (), en forme longue depuis 1875 la République française (), est un État transcontinental souverain, dont le territoire métropolitain est situé en Europe de l'Ouest."