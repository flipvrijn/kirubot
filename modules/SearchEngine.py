import re
import urllib

__author__ = 'flipvanrijn'

class SearchEngine:

    engines = {
        'google': 'http://www.google.com/#q=%s',
        'youtube': 'http://www.youtube.com/results?search_query=%s',
        'wolfram': 'http://www.wolframalpha.com/input/?i=%s',
        'maps': 'http://maps.google.com/maps?q=%s',
        'lmgtfy': 'http://www.lmgtfy.com/?q=%s',
        'imdb': 'http://www.imdb.com/find?q=%s',
        'flickr': 'http://www.flickr.com/search/q=%s',
        'urban': 'http://www.urbandictionary.com/define.php?term=%s',
        'duckduckgo': 'http://www.duckduckgo.com/?q=%s',
        'wikinl': 'http://nl.wikipedia.org/wiki/Speciaal:Zoeken?search=%s',
        'wikien': 'http://en.wikipedia.org/wiki/Special:Search?search=%s',
    }

    def listEngines(self):
        return [k for k in sorted(self.engines.keys())]

    def useEngine(self, engine, term):
        return self.engines.get(engine) % urllib.quote(term, '')

    def parse(self, engine, term):
        for k, v in self.engines.items():
            if engine == k:
                return v % urllib.quote(term, '')