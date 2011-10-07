__author__ = 'flipvanrijn'

import random, json, urllib

types = {
    'getal': lambda x: int(x) < 15 and random.randint(0, 10**int(x)),
    'plaatje': lambda: randomImage()
}

def randomImage():
    fp = urllib.urlopen('http://imgur.com/gallery/new.json')
    jsonContent = json.loads(fp.read())
    randomItem = jsonContent['gallery'][random.randint(0, len(jsonContent['gallery']))]
    return "http://www.imgur.com/" + randomItem['hash'] + randomItem['ext']

def command_gooi(bot, reply, args):
    """
    Gooit een willekeurig type.
    Getal: Gooit een gegeven aantal dobbelstenen.
    Plaatje: Geeft een willekeurig plaatje terug.
    .werp <type> <lengte>
    """
    args = args.split(' ')

    if not args:
        bot.msg(reply, 'Wat moet ik gooien? Beschikbare types: %s' % ", ".join(types))
    elif len(args) == 2:
        if args[0] not in types:
            bot.msg(reply, '\'%s\' ken ik niet. Wat moet ik gooien?' % args[0])
        else:
            bot.msg(reply, str(types[args[0]](args[1])))
    else:
        bot.msg(reply, str(types[args[0]]()))