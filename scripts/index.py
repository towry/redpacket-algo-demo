#!/usr/bin/env python

import os
from os import path
from mako.template import Template

"""
generate the index.hmtl file
"""

class Row(object):
    def __init__(self, title, link):
        self._title = title
        self._link = link

    @property
    def title(self):
        return self._title

    @property
    def link(self):
        return self._link
    
def get_time_num(str):
    n = str.split('-')
    return int(''.join(n[-2:]))

def get_title(str):
    n = str.split('-')
    f = n[-2:]
    ym = n[len(n) - 2]
    md = n[len(n) - 1]
    p = n[0]

    return p + ' ' + ym[:-4] + '/' + ym[4:6] + '/' + ym[-2:] + ' ' + md[:2] + ':' + md[2:4] + ':' + md[-2:]

if __name__ == '__main__':

    root = path.dirname(path.dirname(path.abspath(__file__)))
    assets = path.join(root, "assets")
    template_file = path.join(assets, 'index.html')


    results_folder = path.join(root, "_results")
    results_contents = os.listdir(results_folder)

    items = dict()
    sorts = []
    for sdir in results_contents:
        bnum = get_time_num(sdir)
        sorts.append(bnum)
        row = Row(get_title(sdir), './_results/' + sdir)
        items.update({str(bnum): row})

    sorts.sort()
    sorts.reverse()

    buckets = []
    for b in sorts:
        item = items.get(str(b))
        buckets.append(item)


    contents = Template(filename=template_file, input_encoding="utf-8", output_encoding="utf-8").render(rows=buckets)

    with open(path.join(root, 'index.html'), 'w') as fd:
        fd.write(contents)
