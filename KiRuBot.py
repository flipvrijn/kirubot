__author__ = 'flipvanrijn'

import os, sys, urllib, re
from twisted.words.protocols import irc
from twisted.internet import protocol, threads
from twisted.python import log
from twisted.python.logfile import DailyLogFile

class KiRuBot(irc.IRCClient):
    """ KiRuBot """

    nickname = "KiRuBot"
    cmdchar  = "."

    def connectionMade(self):
        """ Called when the connection has been made. """
        irc.IRCClient.connectionMade(self)
        log.startLogging(DailyLogFile('log.log', './logs'))
        log.msg('Connection made')
    
    def signedOn(self):
        """ Called when bot has signed on. """
        log.msg("Signed on as %s." % self.nickname)
        self.join(self.factory.channel)

    def joined(self, channel):
        """ Called when channel has been joined. """
        log.msg("Joined %s." % channel)

    def privmsg(self, user, channel, msg):
        """
        Called when bot has received a message.
        @param user: nick!user@host
        @param channel: Channel where the message comes from
        @param msg: The message received
        """
        log.msg("%s %s: %s" % (channel, user, msg))
        userParts = user.split('!')
        user = userParts[0]
        reply = channel
        if channel == self.nickname:
            reply = user
        if msg.startswith("."):
            self._command(reply, msg[len(self.cmdchar):])
            return
        
        formulaList = re.findall('\$(.*?)\$', msg)
        if formulaList is not None:
            for formula in formulaList:
                self.msg(reply, 'http://latex.codecogs.com/svg.latex?' + urllib.quote(formula, ''))

    def _command(self, reply, cmnd):
        """ Handles the bot commands. """
        try:
            cmnd, args = cmnd.split(" ", 1)
        except ValueError:
            args = ""

        for module, env in self.factory.modules.items():
            globals, locals = env
            commands = [(c, ref) for c, ref in locals.items() if c == "command_%s" % cmnd]

            for commandName, command in commands:
                d = threads.deferToThread(command, self, reply, args)
    
class KiRuBotFactory(protocol.ClientFactory):

    protocol = KiRuBot
    moduleDir = os.path.join(sys.path[0], "modules/")

    def __init__(self, channel, nickname = 'KiRuBot'):
        self.channel = channel
        self.nickname = nickname
        self.modules = {}

    def startFactory(self):
        self._loadModules()
        log.msg("Factory started.")

    def stopFactory(self):
        protocol.ClientFactory.stopFactory(self)
        log.msg("Factory stopped.")

    def clientConnectionLost(self, connector, reason):
        log.msg("Lost connection (%s), reconnecting." % reason)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        log.msg("Could not connect: %s" % reason)

    def _loadModules(self):
        for module in self._findModules():
            env = self._globals()
            execfile(os.path.join(self.moduleDir, module), env, env)
            self.modules[module] = (env, env)

    def _globals(self):
        g = {}

        return g

    def _findModules(self):
        modules = [m for m in os.listdir(self.moduleDir) if m.startswith("module_") and m.endswith(".py")]
        return modules