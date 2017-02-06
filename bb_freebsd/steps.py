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


class BSDSetMakeEnv(steps.SetPropertyFromCommand):
    '''
    Set the property ``make_env`` from ``make -V``

    :param vars: a list of varaibles. e.g.
        ``['CC', 'CFLAGS', 'CXX', 'CXXFLAGS']``
    :return: a iterable contains some ``steps``
    '''

    name = 'Set make env'

    def __init__(self, vars):
        self.vars = vars

        super(BSDSetMakeEnv, self).__init__(
            command=self.__cmd,
            extract_fn=self.extract,
            strip=False
        )

    @property
    def __cmd(self):
        ret = ['make', '-f', '-', self.makefile]
        for v in self.vars:
            ret.extend(['-V', v])
        return ret

    @property
    def makefile(self):
        lines = (
            '.include <bsd.port.mk>',
        )
        return '\n'.join(lines)

    def extract(self, rc, stdout, stderr):
        vals = stdout.split('\n')
        del vals[-1]

        assert len(self.vars) == len(vals)

        return {
            'make_env': dict(zip(self.vars, vals))
        }
