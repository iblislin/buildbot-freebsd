import shlex

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
    Set the property ``make_env`` from ``make -V MAKE_ENV``

    :param uses: set the ``USES`` macro.  Reference:
        https://www.freebsd.org/doc/en/books/porters-handbook/book.html#uses

    :return: a iterable contains some ``steps``
    '''

    name = 'Set make_env'

    def __init__(self, uses=None):
        self.uses = uses

        super(BSDSetMakeEnv, self).__init__(
            command=self.__cmd,
            extract_fn=self.extract,
            initialStdin=self.makefile,
            strip=True,
        )

    @property
    def __cmd(self):
        return ['make', '-f', '-', '-V', 'MAKE_ENV']

    @property
    def makefile(self):
        lines = (
            ('USES={}'.format(self.uses) if self.uses else ''),
            '.include <bsd.port.mk>',
        )
        return '\n'.join(lines)

    def extract(self, rc, stdout, stderr):
        envs =((k,v) for k, _, v in
               (s.partition('=') for s in shlex.split(stdout)))

        return {
            'make_env': dict(envs)
        }
