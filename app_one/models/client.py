from odoo import models,fields



class Client(models.Model):
    _name = 'client'
    _inherit ='owner'
