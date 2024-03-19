from odoo import models,fields,api
from odoo.exceptions import ValidationError
from datetime import timedelta




class Building(models.Model):
    _name = 'building'
    _description = 'Building'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    number = fields.Integer()
    code = fields.Char()
    description = fields.Text()
    name = fields.Char()

    active = fields.Boolean(default='true',string='active')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'pending'),
        ('sold', 'sold')
    ], default='draft')

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            print(" inside in sold ")
            rec.state = 'sold'

