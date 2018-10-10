### Description
This is the 7th project of OpenClassRoom Python developer course. 

The objective is to develop a Web App with Flask using the Test Driven Development method and APIs.

### Dependencies
- Python 3.6.x
- Flask 1.0.x
- BeautifulSoup4 4.6.x
- Requests 2.19.x
- Pytest 3.8.x (ONLY FOR TESTS)

### How to use
First add in the config.py file and test_gmap.py your google api key.
Then you can run tests.
If all is green run run.py to launch the FlaskApp.

### wiki.py functions

First you have to create a Wiki object.
```python
wiki = Wiki("wikiObj")
```

Get a article with coordinates, tht second parameter is for the range of search
```python
wiki.getArticleWithLocation({1.0,1.0},100)
```

Get a article with name
```python
wiki.getArticleWithName("Paris")
```

Get the first line of the first paragraph on a wiki page. Usually is the first p after the first h2.
```python
wiki.getArticleParagraph("https://fr.wikipedia.org/wiki/Paris")
```

### gmap.py functions

First you have to create a Google Map object.
```python
gmap = Map("gmapObj","your_api_key")
```

Get a location with name
```python
gmap.getLocation("Paris")
```

### strparser.py function

Parse a string to return only address name of location name (Work only in french)
```python
>> parser("Bonjour ! Tu connais Paris ?")
>> "paris"
```