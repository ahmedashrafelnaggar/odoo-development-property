from odoo import models,fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    property_id = fields.Many2one('property')

    # this is inherit method which called button confirm in sale.order, this is way inherit method
    def action_confirm(self):
        rec = super(SaleOrder, self).action_confirm()
        print("inside action_confirm method")
        return rec
