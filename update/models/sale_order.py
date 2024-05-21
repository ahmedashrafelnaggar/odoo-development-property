from odoo.exceptions import ValidationError
from odoo import api, models, _, fields
# from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
