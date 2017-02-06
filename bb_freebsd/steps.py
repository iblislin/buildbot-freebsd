from buildbot.plugins import steps, util


class BSDSysInfo(steps.ShellSequence):
    name = 'FreeBSD System Info'
    alwaysRun = True

    def __init__(self, **kwargs):
        logfile = 'stdio'
        commands = (
            util.ShellArg(command=['freebsd-version'], logfile=logfile),
            util.ShellArg(command=['uname', '-a'], logfile=logfile),
        )

        super(BSDSysInfo, self).__init__(commands=commands, **kwargs)
