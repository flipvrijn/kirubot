__author__ = 'flipvanrijn'

import urllib

def command_pi(bot, reply, args):
    """
    Geeft pi terug met een op te geven nauwkeurigheid. Maximale nauwkeurigheid is 500 decimalen.
    .pi <nauwkeurigheid>
    """

    arg = args.split(' ')[0]

    if not arg:
        bot.msg(reply, 'Een nauwkeurigheid is vereist.')
    else:
        if not arg.isdigit():
            bot.msg(reply, 'I see what you did there!')
        elif int(arg) == 0:
            bot.msg(reply, '4')
        elif int(arg) > 500:
            bot.msg(reply, 'Maximale nauwkeurigheid is 500 decimalen.')
        else:
            fp = urllib.urlopen('http://www.angio.net/pi/digits/10000.txt')
            pi = fp.readline()[0:2+int(arg)]
            bot.msg(reply, pi)
            fp.close()