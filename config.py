import os

if os.environ.get('GOOGLEMAP_KEY') is None:
    GOOGLEMAP_KEY = "AIzaSyCiGYAXBI0xmj1SVqAVYDHUA-6ceTPXbT8"
else:
    GOOGLEMAP_KEY = os.environ['GOOGLEMAP_KEY']


