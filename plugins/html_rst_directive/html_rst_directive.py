# -*- coding: utf-8 -*-
"""
Directive extensions for reStructuredText
=========================================

This plugin allows you to use following directives, that are not
supported by Pelican, within reST documents:

- html
- tip 

Implementation reference:

- See zeyuan's doc 'sphinx' resources page for links

"""

from __future__ import unicode_literals
# Import Docutils document tree nodes module.
from docutils import nodes
# Import Directive base class.
from docutils.parsers.rst import directives, Directive


class RawHtml(Directive):
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True

    def run(self):
        html = ' '.join(self.content)
        node = nodes.raw('', html, format='html')
        return [node]

class TipDirective(Directive):
    final_argument_whitespace = True
    has_content = True

    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content() 
        text = '\n'.join(self.content)
        tip_node = nodes.hint(rawsource=self.content)
        return [tip_node]

def register():
    directives.register_directive('html', RawHtml)
    directives.register_directive('tip', TipDirective)

