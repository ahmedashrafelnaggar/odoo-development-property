from odoo import models,fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cancel_days = fields.Integer(string='Cancel Days', config_parameter='om_hospital.cancel_days')

    # when you create settings in your app you should create new model and inherit from 'res.config.settings'
    # and technical name is base and create file xml and create insid it form view  and action view and menu most things in iy is fixed