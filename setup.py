#!/usr/bin/env python3

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

setup(
    name='lxd-backup',
    version='0.1.0',
    license='MIT License',
    description='Tool to automatically backup lxd containers',
    author='Alex Peyrard',
    author_email='alex.peyrard@gmail.com',
    url='https://github.com/apeyrard/lxd-backup',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Environment :: No Input/Output (Daemon)',
        'Framework :: Pytest',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
    keywords=[
    ],
    install_requires=[
        'pylxd>=2.2.6',
        'arrow>=0.10.0',
        'boto3>=1.4.2',
    ],
    extras_require={
    },
    entry_points={
        'console_scripts': [
            'lxd-backup = lxd_backup.cli:main',
        ],
    },
)
