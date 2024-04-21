# -*- coding: utf-8 -*-
# from odoo import http


# class OmOdooInheritence(http.Controller):
#     @http.route('/om_odoo_inheritence/om_odoo_inheritence', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/om_odoo_inheritence/om_odoo_inheritence/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('om_odoo_inheritence.listing', {
#             'root': '/om_odoo_inheritence/om_odoo_inheritence',
#             'objects': http.request.env['om_odoo_inheritence.om_odoo_inheritence'].search([]),
#         })

#     @http.route('/om_odoo_inheritence/om_odoo_inheritence/objects/<model("om_odoo_inheritence.om_odoo_inheritence"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('om_odoo_inheritence.object', {
#             'object': obj
#         })

