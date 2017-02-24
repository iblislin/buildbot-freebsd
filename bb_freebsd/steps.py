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


class BSDSetMakeVar(steps.SetPropertyFromCommand):
    '''
    Set the property ``name`` from ``make -V VAR``

    :param names: list of property names
    :param vars: list of variable names
    :param uses: set the ``USES`` macro.  Reference:
        https://www.freebsd.org/doc/en/books/porters-handbook/book.html#uses
    '''

    def __init__(self, names, vars, uses=None, **kwargs):
        self.names = names
        self.name = 'Set {}'.format(', '.join(names))
        self.vars = vars
        self.uses = uses

        super(BSDSetMakeVar, self).__init__(
            command=self.__cmd,
            extract_fn=self.extract,
            initialStdin=self.makefile,
            strip=False,
            **kwargs
        )

    @property
    def __cmd(self):
        return ['make', '-f', '-'] + ['-V{}'.format(v) for v in self.vars]

    @property
    def makefile(self):
        lines = (
            ('USES={}'.format(self.uses) if self.uses else ''),
            '.include <bsd.port.mk>',
        )
        return '\n'.join(lines)

    def extract(self, rc, stdout, stderr):
        return dict(zip(self.names, stdout.split('\n')))


class BSDSetMakeEnv(BSDSetMakeVar):
    '''
    Set the property ``make_env`` from ``make -V MAKE_ENV``
    '''
    def __init__(self, **kwargs):
        super(BSDSetMakeEnv, self).__init__(
            ['make_env'],
            ['MAKE_ENV'],
            **kwargs
        )

    def extract(self, rc, stdout, stderr):
        envs =((k,v) for k, _, v in
               (s.partition('=') for s in shlex.split(stdout)))

        return {
            'make_env': dict(envs)
        }
