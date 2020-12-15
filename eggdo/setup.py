#!/usr/bin/env python
# Source: https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-setup-script
# Via: https://www.samueldowling.com/2020/06/08/how-to-set-up-a-python-project-and-development-environment/  # noqa
# -*- encoding: utf-8 -*-
import io
from os.path import dirname
from os.path import join

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


version = "0.0.1"


setup(
    name='Egg-Todo-List-Preocts',
    version=version,
    license='GNU General Public License',
    description='A complexly simple do-to list',
    author='Preocts',
    author_email='preocts@preocts.com',
    url='https://github.com/Preocts',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
    # entry_points={
    #     'console_scripts': [
    #         'eggdo = eggdo.__main__:main',
    #     ]
    # },
    include_package_data=False
)
