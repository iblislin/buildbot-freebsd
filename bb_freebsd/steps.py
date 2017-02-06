from buildbot.plugins import steps, util


class BSDSysInfo(steps.ShellSequence):
    describe = 'FreeBSD System Info'

    def __init__(self):
        logfile = 'sysinfo'
        commands = (
            util.ShellArg(command=['uname', '-a'], logfile=logfile),
            util.ShellArg(command=['freebsd-version'], logfile=logfile),
        )
        super(BSDSysInfo, self).__init__(commands=commands)
