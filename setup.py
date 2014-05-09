# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='gridwidget',
    version='0.1',
    description='An IPython widget for simple bootstrap fluid grid layouts',
    author='Jonathan Frederic',
    author_email='jon.freder@gmail.com',
    license='MIT License',
    url='https://github.com/jdfreder/ipython-gridwidget',
    keywords='data visualization interactive interaction python ipython widgets widget',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python :: 2.7',
                 'License :: OSI Approved :: MIT License'],
    packages=['gridwidget'],
    package_data={'': ['*.js']}
)
