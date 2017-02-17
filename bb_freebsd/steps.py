import shlex

from buildbot.plugins import steps, util


class BSDSysInfo(steps.ShellSequence):
    name = 'FreeBSD System Info'
    alwaysRun = True
    logEnviron = False

    def __init__(self, pkginfo=False, pkgs=None, **kwargs):
        logfile = 'stdio'
        commands = [
            util.ShellArg(command=['freebsd-version'], logfile=logfile),
            util.ShellArg(command=['uname', '-a'], logfile=logfile),
        ]

        if pkginfo:
            commands.append(
                util.ShellArg(command=['pkg', 'info'], logfile='pkg'),
            )
            if pkgs:
                commands.extend([self.pkg_info(pkg) for pkg in pkgs])

        super(BSDSysInfo, self).__init__(commands=commands, **kwargs)

    def pkg_info(self, pkg):
        return util.ShellArg(command=['pkg', 'info', pkg],
                             logfile='pkg-{}'.format(pkg))


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
