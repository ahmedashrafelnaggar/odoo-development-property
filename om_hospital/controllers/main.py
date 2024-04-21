# from odoo import http
# from odoo.http import request
#
#
# class Hospital(http.Controller):
#
#     @http.route("/hospital/patient", method=["Get"], type="http", auth="public", csrf=False)
#     def patient_endpoint(self, **kw):
#         # patients = request.env['models_name'].sudo().search([ ])
#         patients = request.env['hospital.patient'].sudo().search([])
#         # return request.render("module_name.template_id", values)
#         return request.render("om_hospital.patients_page", {
#             'patients': patients
#         })


