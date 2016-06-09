# -*- coding: utf-8 -*-

from openerp import models, fields, api

import os

def file_get_contents(filename):
  if os.path.exists(filename):
    fp = open(filename, "r")
    content = fp.read()
    fp.close()
    return content

class importardor(models.Model):
    _name = 'importador'

    def run(self, file):
        exec file_get_contents(file)