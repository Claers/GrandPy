from flask import Flask,render_template,request, make_response
import json
import os

from .wiki import *
from .strparser import parser
from .gmap import *


app = Flask(__name__)
app.config.from_pyfile('../config.py')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def ins():
     data = request.form['keyword']
     resp = make_response(json.dumps(getResp(data)))
     resp.status_code = 200
     resp.headers['Access-Control-Allow-Origin'] = '*'
     return resp

def getResp(query):
	wikiO = Wiki("wiki")
	map = Map("map",app.config["GOOGLEMAP_KEY"])

	string = query
	string = parser(string)
	if(string != ""):
		loc = map.getLocation(string)
		if(loc != "Nothing" and loc != "AccessDenied"):
			articleUrl = ""
			wikiO.article = wikiO.getArticle(loc['result']['geometry']['location'],"1000")
			if(wikiO.article == {'batchcomplete': ''}):
				wikiO.article = wikiO.getArticle(loc['result']['geometry']['location'],"10000")
			if(wikiO.article != {'batchcomplete': ''}):
				for article in wikiO.article['query']['pages']:
					if wikiO.article['query']['pages'][article]['title'] in loc['result']['formatted_address']:
						articleUrl = wikiO.article['query']['pages'][article]['fullurl']
						articleName = wikiO.article['query']['pages'][article]['title']
				if(articleUrl != ""):
					articledesc = wikiO.getArticleDesc(articleName)
					articleParagraph = wikiO.getArticleParagraph(articleUrl)
					return [loc,articleUrl,articleParagraph]
				else:
					for article in wikiO.article['query']['pages']:
						articleUrl = wikiO.article['query']['pages'][article]['fullurl']
						articleName = wikiO.article['query']['pages'][article]['title']
					print(articleUrl)
					if(articleUrl != ""):
						articledesc = wikiO.getArticleDesc(articleName)
						articleParagraph = wikiO.getArticleParagraph(articleUrl)
						print(article)
						print(articleParagraph)
						return [loc,articleUrl,articleParagraph]
			else:
				return 'NoArticle'
		elif(loc == "Nothing"):
			return "error"
		elif(loc == "AccessDenied"):
			return "AccessDenied"
	else:
		return "error"

app.jinja_env.globals.update(getResp=getResp)
