__author__ = 'flipvanrijn'

def command_help(bot, reply, args):
    """
    Print een lijst van commands en help voor individuele commands:
    .help en .help <command>
    """

    commands = []
    for module, env in bot.factory.modules.items():
        globals, locals = env
        commands += [(c.replace("command_", ""), ref) for c, ref in locals.items() if c.startswith("command_")]
    if len(args) > 0:
        for cname, ref in commands:
            if cname == args:
                helptext = ref.__doc__
                bot.msg(reply, helptext)
                return
    else:
        commandlist = ", ".join([c for c, ref in commands])
        bot.msg(reply, ".help <command> voor meer. \nBeschikbare commands: %s" % commandlist)