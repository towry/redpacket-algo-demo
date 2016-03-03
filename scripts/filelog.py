# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime
from scripts.template import template



class Filelog(object):
    """Filelog"""
    def __init__(self, basepath, prefix=None):
        self._basepath = basepath
        self._count = 0
        self._folder = None
        self._fd = None
        self._round = 0
        self._prefix = prefix
        self._tpl_data = dict()

        self._make_dir()

    def _make_dir(self):
        prefix = self._prefix if self._prefix is not None else ''
        prefix = prefix + '-'
        pname = prefix + 'rounds-' + _get_time_fname()
        format = u"%Y年%m月%d日"
        self._tpl_data['round_name'] = prefix + 'rounds-' + (datetime.now().strftime(format.encode('utf-8'))).decode('utf-8')
        self._tpl_data['parent_uri'] = pname
        pfull_name = os.path.join(self._basepath, pname)
        ok = _make_dir(pfull_name)
        if not ok:
            raise Exception("{} folder already exists.".format(pname))
        self._folder = pfull_name

    def _make_fd(self, ext=None, fname=None):
        ext = '.txt' if ext is None else ext
        self._fd = open(os.path.join(self._folder, fname if fname else ('round-' + str(self._count) + ext)), 'a')
        self._tpl_data['json_uri'] = 'round-' + str(self._count) + ext

    def _close_fd(self):
        if self._fd is None:
            return
        self._fd.close()
        self._fd = None

    def _json(self, array):
        output = array
        outstr = json.dumps(output)
        self._count += 1
        self._close_fd()
        self._make_fd('.json')
        self.writeln(outstr)
        self._close_fd()
        template_output = template(**self._tpl_data)
        self._make_fd(None, 'index.html')
        self.writeln(template_output)
        self._close_fd()

    def done(self):
        self._close_fd()
        self._count = 0
        self._round = 0

    def round(self, array, json_only=False):
        if json_only:
            return self._json(array)

        total_len = len(array)
        array.sort()

        if self._round > 10:
            self._round = 0
            self._count += 1
            self._close_fd()
            self._make_fd()

        if self._fd is None:
            self._make_fd()
        self.writeln('length: ' + str(total_len))
        self.writeln('result: ')
        
        turn = 0
        for item in array:
            if turn is 12:
                self.writeln()
                turn = 0
            turn += 1
            self.write("{:.2f}".format(item) + ', ')
        self.writeln()
        self.writeln()
        self._round += 1

    def writeln(self, content=None):
        content = '\n' if content is None else content
        self.write(content)
        if content is '\n':
            return
        self.write('\n')

    def write(self, content):
        self._fd.write(content)

def _get_time_fname():
    now = datetime.now()
    time = now.strftime("%Y%m%d-%H%M%S")
    return time

def _make_dir(path):
    if os.path.exists(path):
        return False
    os.makedirs(path)
    return True
