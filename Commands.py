import SearchEngine
from time import gmtime, strftime

__author__ = 'flipvanrijn'

class Commands:
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
                searchEnginesParsed = se.parse(commandParts[0], commandParts[1])
                if searchEnginesParsed:
                    self.msg(user, searchEnginesParsed)

    def COMMAND_tijd(self, user, channel, msg):
        """
        Print de huidige datum en tijd. \
        .tijd
        """
        self.msg(user, strftime("%A %d %B %Y %H:%M:%S GMT+1", gmtime()))