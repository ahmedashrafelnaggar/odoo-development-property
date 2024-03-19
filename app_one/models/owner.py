from odoo import models,fields,api
from odoo.exceptions import ValidationError




class Owner(models.Model):
    _name = 'owner'

    name = fields.Char()
    phone = fields.Char()
    address = fields.Char()
    description = fields.Text()
    property_ids = fields.One2many('property', 'owner_id', ondelete='cascade')


    _sql_constraints = [('name_unique', 'unique("name")', "this name is exist!"),]
