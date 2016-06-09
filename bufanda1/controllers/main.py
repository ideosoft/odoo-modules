# -*- coding: utf-8 -*-
from openerp import http

# class Bufanda1(http.Controller):
#     @http.route('/bufanda1/bufanda1/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bufanda1/bufanda1/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bufanda1.listing', {
#             'root': '/bufanda1/bufanda1',
#             'objects': http.request.env['bufanda1.bufanda1'].search([]),
#         })

#     @http.route('/bufanda1/bufanda1/objects/<model("bufanda1.bufanda1"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bufanda1.object', {
#             'object': obj
#         })