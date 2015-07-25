#!/usr/bin/env python

from distutils.core import setup

setup(name='lnotes',
      version='1.0',
      description='Personal wiki',
      author='Stanislav Bohm',
      url='',
      packages=['lnotes'],
      package_dir = { 'lnotes' : 'src' },
      package_data = { 'lnotes' : [ 'static/asciidoc.css',
                                    'templates/*.html' ] }

 #     """[('templates', ['templates/page.html',
 #                                'templates/notfound.html',
 #                                'templates/tree.html', ]),
 #                 ('static', ['static/asciidoc.css']) ]"""
     )
