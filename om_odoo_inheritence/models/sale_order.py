from odoo import models,fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_user_id = fields.Many2one('res.users', tracking=1)

    # this is inheriting method which called button confirm in sale.order, this is way inherit method
    def action_confirm(self):
        rec = super(SaleOrder, self).action_confirm()
        print("success")
        self.confirmed_user_id = self.env.user.id
        return rec




