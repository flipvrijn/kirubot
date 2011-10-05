__author__ = 'flipvanrijn'

from time import gmtime, strftime

def command_tijd(bot, reply, args):
    """
    Print de huidige datum en tijd.
    .tijd
    """
    bot.msg(reply, strftime("%A %d %B %Y %H:%M:%S GMT+1", gmtime()))