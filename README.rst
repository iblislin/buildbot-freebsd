buildbot-freebsd
===============================================================================

A Buildbot_ plugin for FreeBSD_.

.. _Buildbot: https://buildbot.net/
.. _FreeBSD: https://www.freebsd.org/


Installation
----------------------------------------------------------------------

::

    pip install git+https://github.com/iblis17/buildbot-freebsd.git


Sample Usage
----------------------------------------------------------------------

.. code-block:: python

	factory.addSteps([
		steps.BSDSysInfo(
            pkginfo=True,
            pkgs=[
                'llvm38',
                'libunwind',
                'pcre2',
            ]),
		steps.BSDSetMakeVar(['make_jobs'], ['MAKE_JOBS_NUMBER']),
		steps.BSDSetMakeEnv(uses='fortran'),

		steps.GitHub(
			repourl='git://...',
			mode='full',
			method='fresh'),

		steps.Compile(
			command=['make', 'all', '-j', util.Property('make_jobs')],
			env=util.Property('make_env')),  # set FC, FFLAGS, etc properly
	])


``steps``
----------------------------------------------------------------------

BSDSysInfo
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A Simple ``ShellSequence`` that invokes

- ``freebsd-version``

- ``uname -a``

- ``pkg info``: *optional*. Enabled via ``pkginfo=True```


BSDSetMakeVar
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Set the property ``name`` from ``make -V VAR``.

By default the ``Makefile`` read by ``make``::

    .include <bsd.port.mk>

So this step will require that there is a ports tree on worker.

Parameters:

:names: list of property names
:vars: list of variable names
:uses: set the ``USES`` macro in ``Makefile``.
    Reference:
    https://www.freebsd.org/doc/en/books/porters-handbook/book.html#uses


BSDSetMakeEnv
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This step will set a property ``make_env`` to the result
of ``make -V MAKE_ENV``. This property will be a python dictionary.

By default the ``Makefile`` read by ``make``::

    .include <bsd.port.mk>

So this step will require that there is a ports tree on worker.

Parameters:

:uses: set the ``USES`` macro in ``Makefile``.
    Reference:
    https://www.freebsd.org/doc/en/books/porters-handbook/book.html#uses


LICENSE
----------------------------------------------------------------------

MIT
