import urllib
import re
import SearchEngine
from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.python import log
from twisted.python.logfile import DailyLogFile
from time import gmtime, strftime

__author__ = 'flipvanrijn'

class KiRuBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        log.startLogging(DailyLogFile.fromFullPath('/Users/flipvanrijn/PyCharmProjects/bot/log.log'))
        self.commands = filter(
            lambda x: x.find('COMMAND_') != -1,
            dir(self.__class__)
        )
        log.msg('Connection made')
    
    def signedOn(self):
        log.msg("Signed on as %s." % self.nickname)
        self.join(self.factory.channel)

    def joined(self, channel):
        log.msg("Joined %s." % channel)

    def privmsg(self, user, channel, msg):
        log.msg("%s %s: %s" % (channel, user, msg))
        userParts = user.split('!')
        user = userParts[0]
        if channel == self.nickname:
            channel = user
        if msg[0] == '.':
            self.commandHandler(channel, channel, msg[1:])
            return
        # Parse formulas
        formulaList = re.findall('\$(.*?)\$', msg)
        if formulaList is not None:
            for formula in formulaList:
                self.msg(channel, 'http://latex.codecogs.com/svg.latex?' + urllib.quote(formula, ''))

    def COMMAND_help(self, user, channel, msg):
        """
        Print een lijst van commands en help voor individuele commands: \
        .help and .help <command>
        """
        if not len(msg):
            returnMsg = '.help <command> voor meer. Beschikbare commands: '
            for command in self.commands:
                returnMsg += '%s ' % command[len('COMMAND_'):]
            self.msg(user, returnMsg)
        elif 'COMMAND_' + msg in self.commands:
            returnMsg = '%s' % (
                getattr(self.__class__, 'COMMAND_%s' % msg).__doc__.strip()
            )
            self.msg(user, returnMsg)
        else:
            self.msg(user, 'Command \'%s\'ken ik niet.' % msg)

    def COMMAND_zoek(self, user, channel, msg):
        """
        Print een link naar een zoekmachine naar keuze die naar de zoekresultaten leidt van de opgegeven zoek term. \
        .zoek <zoekmachine> <term>
        """
        if not len(msg):
            return
        commandParts = msg.split(' ')
        se = SearchEngine.SearchEngine()
        if len(commandParts) < 2:
            self.msg(user, 'Er is een zoekterm nodig.')
        else:
            searchEngines = se.listEngines()
            if commandParts[0] not in searchEngines:
                self.msg(user, 'Zoekmachine \'%s\' ken ik niet. Beschikbare zoekmachines: %s' % (commandParts[0], ", ".join(searchEngines)))
            else:
                searchEnginesParsed = se.parse(commandParts[0], ' '.join(commandParts[1:]).strip())
                if searchEnginesParsed:
                    self.msg(user, searchEnginesParsed)

    def COMMAND_tijd(self, user, channel, msg):
        """
        Print de huidige datum en tijd. \
        .tijd
        """
        self.msg(user, strftime("%A %d %B %Y %H:%M:%S GMT+1", gmtime()))

    def COMMAND_tinyurl(self, user, channel, msg):
        """
        Maakt van een lange link een korte link. \
        .tinyurl <link>
        """
        if '://' not in msg:
            msg = "http://" + msg
        fp = urllib.urlopen('http://www.tinyurl.com/api-create.php?url=' + msg)
        self.msg(user, fp.readline())
        fp.close()
    
    def commandHandler(self, user, channel, msg):
        log.msg('handle command: %s' % msg)
        commandParts = msg.split(' ')
        command = commandParts[0]
        if 'COMMAND_' + command in self.commands:
            getattr(self.__class__, 'COMMAND_%s' % command)(
                self,
                user,
                channel,
                ' '.join(commandParts[1:]).strip(),
            )

class KiRuBotFactory(protocol.ClientFactory):
    protocol = KiRuBot

    def __init__(self, channel, nickname = 'KiRuBot'):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        log.msg("Lost connection (%s), reconnecting." % reason)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        log.msg("Could not connect: %s" % reason)