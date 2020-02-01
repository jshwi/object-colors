import os
import sys
sys.path.append(os.path.abspath('../'))
project = u'Object Colors'
copyright = u'2019, Stephen Whitlock'
author = u'Stephen Whitlock'
release = '1.0.8'
source_suffix = ['.rst']
master_doc = 'index'
exclude_patterns = ['_build']
templates_path = ['_templates']
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
    'sphinx.ext.imgmath',
    'sphinx.ext.doctest'

]
todo_include_todos = True
pygments_style = 'monokai'
autoclass_content = "both"
autodoc_member_order = 'bysource'
autodoc_default_options = {"members": None}
imgmath_latex_preamble = r'''
\usepackage{xcolor}
\definecolor{offwhite}{rgb}{238,238,238}
\everymath{\color{offwhite}}
\everydisplay{\color{offwhite}}
'''

html_theme = 'graphite'
html_theme_path = ['.']
html_static_path = ['_static']
html_logo = '_static/oc.png'
html_sidebars = {
    '**': [
        'globaltoc.html',
        'searchbox.html'
    ]
}
