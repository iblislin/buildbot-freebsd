import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

import bb_freebsd as bsd


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def get_requires():
    src_dir = os.path.dirname(__file__)
    with open(os.path.join(src_dir, 'requirements.txt')) as f:
        return tuple(map(str.strip, f.readlines()))


setup(
    name='buildbot-freebsd',
    version=bsd.version,
    author='Iblis Lin',
    author_email='Iblis Lin',
    maintainer='Iblis Lin',
    maintainer_email='iblis@hs.ntnu.edu.tw',
    url='',
    packages=find_packages(exclude=['tests']),
    entry_points = {
        'buildbot.steps': [
            'BSDSysInfo = bb_freebsd.steps:BSDSysInfo',
            'BSDSetMakeEnv = bb_freebsd.steps:BSDSetMakeEnv',
        ],
        'buildbot.util': [
            'freebsd = bb_freebsd.util',
        ]
    },
    # install_requires=get_requires(),
    tests_require=['coverage', 'pytest', 'pytest-cov', 'tox', 'mock'],
    cmdclass={'test': PyTest},
    keywords='buildbot,freebsd',
    # description=''
    # long_description='',
    # download_url='',
    platforms=['FreeBSD'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
