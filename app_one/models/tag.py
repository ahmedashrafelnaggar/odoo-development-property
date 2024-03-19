from odoo import models,fields



class Tag(models.Model):
    _name = 'tag'

    name = fields.Char(reqiured=1)
