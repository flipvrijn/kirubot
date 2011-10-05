__author__ = 'flipvanrijn'

import urllib

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

def listEngines():
    return [k for k in sorted(engines.keys())]

def useEngine(engine, term):
    return engines.get(engine) % urllib.quote(term, '')

def parse(engine, term):
    for k, v in engines.items():
        if engine == k:
            return v % urllib.quote(term, '')

def command_zoek(bot, reply, args):
    """
    Print een link naar een zoekmachine naar keuze die naar de zoekresultaten leidt van de opgegeven zoek term.
    Indien geen zoekmachine meegegeven is, wordt standaard op Google gezocht.
    .zoek <zoekmachine> <term>
    """
    if not args:
        return
    args = args.split(' ')
    engineUnkown = 'Zoekmachine \'%s\' ken ik niet. Beschikbare zoekmachines: %s'
    if len(args) < 2:
        if args[0] not in listEngines():
            bot.msg(reply, useEngine('google', ' '.join(args[0:]).strip()))
        else:
            bot.msg(reply, 'Er is een zoekterm nodig.')
    else:
        if args[0] not in listEngines():
            bot.msg(reply, engineUnkown % (args[0], ", ".join(listEngines())))
        else:
            searchEnginesParsed = parse(args[0], ' '.join(args[1:]).strip())
            if searchEnginesParsed:
                bot.msg(reply, searchEnginesParsed)