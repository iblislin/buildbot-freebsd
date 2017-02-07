buildbot-freebsd
===============================================================================

The buildbot plugin for freebsd.


Installation
----------------------------------------------------------------------

::

    pip install git+https://github.com/iblis17/buildbot-freebsd.git


Sample Usage
----------------------------------------------------------------------

.. code-block:: python

	factory.addSteps([
		steps.BSDSysInfo(),
		steps.BSDSetMakeEnv(uses='fortran'),

		steps.GitHub(
			repourl='git://...',
			mode='full',
			method='fresh'),

		steps.Compile(
			command=['make', 'all'],
			env=util.Property('make_env')),  # set FC, FFLAGS, etc properly
	])


``steps``
----------------------------------------------------------------------

BSDSysInfo
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A Simple ``ShellSequence`` that invokes

- ``freebsd-version``

- ``uname -a``


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
