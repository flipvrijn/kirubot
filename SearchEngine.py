import re
import urllib

__author__ = 'flipvanrijn'

class SearchEngine:

    engines = dict({
        'google': 'http://www.google.com/#q=%s',
        'youtube': 'http://www.youtube.com/results?search_query=%s',
        'wolfram': 'http://www.wolframalpha.com/input/?i=%s',
        'maps': 'http://maps.google.com/maps?q=%s',
        'lmgtfy': 'http://www.lmgtfy.com/?q=%s',
        'imdb': 'http://www.imdb.com/find?q=%s',
        'flickr': 'http://www.flickr.com/search/q=%s',
        'urban': 'http://www.urbandictionary.com/define.php?term=%s',
        'duckduckgo': 'http://www.duckduckgo.com/?q=%s'
    })

    def __init__(self):
        pass

    def listEngines(self):
        return list(self.engines.viewkeys())

    def parse(self, engine, term):
        for k, v in self.engines.items():
            if engine == k:
                return v % urllib.quote(term, '')