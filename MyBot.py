__author__ = 'flipvanrijn'

from twisted.internet import reactor
from KiRuBot import *

if __name__ == "__main__":
    reactor.connectTCP('irc.ai.ru.nl', 6667, KiRuBotFactory('#kiru'))
    reactor.run()