from odoo import api, fields, models, _
from datetime import datetime, date


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Hospital Tag"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string='Name', tracking=1,required=1)
    active = fields.Boolean(string='Active', default=True, copy=False)
    color = fields.Integer(string='Color')
    color2 = fields.Char(string='Color2')
    sequence = fields.Char(string='sequence')

     # when you write function copy you should put it before sql constraints , this method to do duplicate for any form
    # and if you want to say make any form (copy) active = false , this mean write attribute copy=false , in active field
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s(copy)", self.name)
            default['sequence'] = 10
        return super(PatientTag, self).copy(default)

    # when you use sql constrain you should create  new database and should admin_passwd = admin in file odoo.conf
    _sql_constraints = [
        ('name_unique', 'unique("name")', "this name is exist!"),
        ('check_sequence', 'check(sequence > 0)', "sequence must be positive number!"),
        # ('name_unique', 'unique("name", "active")', "this name is exist!"),
    ]

