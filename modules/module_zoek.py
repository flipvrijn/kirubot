__author__ = 'flipvanrijn'

import SearchEngine

def command_zoek(bot, reply, args):
    """
    Print een link naar een zoekmachine naar keuze die naar de zoekresultaten leidt van de opgegeven zoek term.
    Indien geen zoekmachine meegegeven is, wordt standaard op Google gezocht.
    .zoek <zoekmachine> <term>
    """
    if not args:
        return
    args = args.split(' ')
    se = SearchEngine.SearchEngine()
    searchEngines = se.listEngines()
    strEngineUnkown = 'Zoekmachine \'%s\' ken ik niet. Beschikbare zoekmachines: %s'
    if len(args) < 2:
        if args[0] not in searchEngines:
            bot.msg(reply, se.useEngine('google', ' '.join(args[0:]).strip()))
        else:
            bot.msg(reply, 'Er is een zoekterm nodig.')
    else:
        if args[0] not in searchEngines:
            bot.msg(reply, strEngineUnkown % (args[0], ", ".join(searchEngines)))
        else:
            searchEnginesParsed = se.parse(args[0], ' '.join(args[1:]).strip())
            if searchEnginesParsed:
                bot.msg(reply, searchEnginesParsed)