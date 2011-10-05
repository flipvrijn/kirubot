__author__ = 'flipvanrijn'

import urllib

def command_tinyurl(bot, reply, args):
    """
    Maakt van een lange link een korte link.
    .tinyurl <link>
    """

    arg = args.split(' ')[0]

    if '://' not in arg:
        arg = 'http://' + arg
    fp = urllib.urlopen('http://www.tinyurl.com/api-create.php?url=' + arg)
    bot.msg(reply, fp.readline())
    fp.close()