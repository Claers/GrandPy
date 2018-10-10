from flask import Flask, render_template, request, make_response
import json
import os

from .wiki import *
from .strparser import parser
from .gmap import *


app = Flask(__name__)  # Create the Flask app
app.config.from_pyfile('../config.py')  # Set the config file


@app.route('/')  # On localhost:5000/ return that
def index():
    return render_template('index.html')  # Return the html template


@app.route('/', methods=['POST'])  # On localhost:5000/ post method return that
def ins():
    data = request.form['keyword']  # Get the data
    # Make a response and manipulate data
    resp = make_response(json.dumps(getResp(data)))
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def getResp(query):  # The function used for data manipulation
    wikiO = Wiki("wiki")  # Create a wiki object
    map = Map("map", app.config["GOOGLEMAP_KEY"])  # Create a googlemap object

    string = query
    string = parser(string)  # Parse the query with the parser function
    if(string != ""):
        # First try to get a location on the map with google maps
        loc = map.getLocation(string)
        if(loc != "Nothing" and loc != "AccessDenied"):
            articleUrl = ""
            # Second try ro get a wiki article with the name of the location
            wikiO.article = wikiO.getArticleWithName(string)
            if(wikiO.article != None):
                # If the name of the article isn't similiar with the location
                # address skip
                if(wikiO.article[1][0] in loc['result']['formatted_address']):
                    articleUrl = unquote(wikiO.article[3][0])
                    articleParagraph = wikiO.getArticleParagraph(articleUrl)
                    return [loc, articleUrl, articleParagraph]
                else:
                        # Third try to get a article with the full address
                    wikiO.article = wikiO.getArticleWithName(
                        loc['result']['formatted_address'])
                    if(wikiO.article != None):
                        # If the name of the article isn't similiar with the location
                        # address skip
                        if(wikiO.article[1][0] in loc['result']['formatted_address']):
                            articleUrl = unquote(wikiO.article[3][0])
                            articleParagraph = wikiO.getArticleParagraph(
                                articleUrl)
                            return [loc, articleUrl, articleParagraph]
                    else:
                        # Fourth try to get an article with the coordinates
                        wikiO.article = wikiO.getArticleWithLocation(
                            loc['result']['geometry']['location'], "1000")
                        # If no article is found try with a highter range
                        if(wikiO.article == {'batchcomplete': ''}):
                            wikiO.article = wikiO.getArticleWithLocation(
                                loc['result']['geometry']['location'], "10000")
                        if(wikiO.article != {'batchcomplete': ''}):
                            for article in wikiO.article['query']['pages']:
                                # If the article name is found in the address
                                if wikiO.article['query']['pages'][article]['title'] in loc['result']['formatted_address']:
                                    articleUrl = wikiO.article['query'][
                                        'pages'][article]['fullurl']
                                    articleName = wikiO.article['query'][
                                        'pages'][article]['title']
                            if(articleUrl != ""):
                                articleParagraph = wikiO.getArticleParagraph(
                                    articleUrl)
                                return [loc, articleUrl, articleParagraph]
                            else:
                                articleUrl = ""
                                for article in wikiO.article['query']['pages']:
                                    if(articleUrl == ""):  # Catch the first article of the list
                                        articleUrl = wikiO.article['query'][
                                            'pages'][article]['fullurl']
                                        articleName = wikiO.article['query'][
                                            'pages'][article]['title']
                                articleParagraph = wikiO.getArticleParagraph(
                                    articleUrl)
                                return [loc, articleUrl, articleParagraph]
                        else:
                            return [loc, 'NoTxt']  # If no article is found
            else:
                return [loc, 'NoTxt']  # If no article is found
        elif(loc == "Nothing"):
            return "error"  # If nothing is found
        elif(loc == "AccessDenied"):
            return "AccessDenied"  # If google maps raised a access error
    else:
        return "error"  # If the parsed query is empty

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
