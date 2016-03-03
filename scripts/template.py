# -*- coding: utf-8 -*-

from os import path
from mako.template import Template

root = path.dirname(path.dirname(path.abspath(__file__)))
assets = path.join(root, "assets")
template_file = path.join(assets, 'template.html')

template_str = None

with open(template_file, 'r') as fd:
    template_str = fd.read()

def template(**args):
    return Template(template_str.encode('utf-8'), input_encoding='utf-8', output_encoding='utf8').render(**args)
