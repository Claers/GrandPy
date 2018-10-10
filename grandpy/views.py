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
			wikiO.article = wikiO.getArticleWithName(string)
			if(wikiO.article != None):
				if(wikiO.article[1][0] in loc['result']['formatted_address']):
					articleUrl = unquote(wikiO.article[3][0])
					articleParagraph = wikiO.getArticleParagraph(articleUrl)
					return [loc,articleUrl,articleParagraph]
				else:
					wikiO.article = wikiO.getArticleWithName(loc['result']['formatted_address'])
					if(wikiO.article != None):
						if(wikiO.article[1][0] in loc['result']['formatted_address']):
							articleUrl = unquote(wikiO.article[3][0])
							articleParagraph = wikiO.getArticleParagraph(articleUrl)
							return [loc,articleUrl,articleParagraph]
					else:
						wikiO.article = wikiO.getArticleWithLocation(loc['result']['geometry']['location'],"1000")
						if(wikiO.article == {'batchcomplete': ''}):
							wikiO.article = wikiO.getArticleWithLocation(loc['result']['geometry']['location'],"10000")
						if(wikiO.article != {'batchcomplete': ''}):
							for article in wikiO.article['query']['pages']:
								if wikiO.article['query']['pages'][article]['title'] in loc['result']['formatted_address']:
									articleUrl = wikiO.article['query']['pages'][article]['fullurl']
									articleName = wikiO.article['query']['pages'][article]['title']
							if(articleUrl != ""):
								articleParagraph = wikiO.getArticleParagraph(articleUrl)
								return [loc,articleUrl,articleParagraph]
							else:
								for article in wikiO.article['query']['pages']:
									articleUrl = wikiO.article['query']['pages'][article]['fullurl']
									articleName = wikiO.article['query']['pages'][article]['title']
								articleParagraph = wikiO.getArticleParagraph(articleUrl)
								return [loc,articleUrl,articleParagraph]
						else:
							return [loc,'NoTxt']
			else:
				return [loc,'NoTxt']
		elif(loc == "Nothing"):
			return "error"
		elif(loc == "AccessDenied"):
			return "AccessDenied"
	else:
		return "error"

app.jinja_env.globals.update(getResp=getResp)
