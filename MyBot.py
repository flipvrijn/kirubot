from twisted.internet import reactor
from KiRuBot import *

__author__ = 'flipvanrijn'

if __name__ == "__main__":
    reactor.connectTCP('irc.ai.ru.nl', 6667, KiRuBotFactory('#bottest'))
    reactor.run()