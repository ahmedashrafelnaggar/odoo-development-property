from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    line_ids = fields.One2many('purchase.order.line', 'purchase_id', ondelete="cascade")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    amount_total = fields.Monetary(string='Total PO', store=True, readonly=True, compute='_amount_all')
    total_billed = fields.Integer(string=' Total Billed ', copy=False, default=0, store=True)
    average_cost = fields.Float(store=True, readonly=True)
    total_to_be_billed = fields.Float(string="Total to be Billed")
    percentage_of_investigator = fields.Float(string=" Invest Percentage")
    percentage_of_uninvestigator = fields.Float(string=" Un invest Percentage")




class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    purchase_id = fields.Many2one('purchase.order', ondelete="cascade")
    product_id = fields.Many2one('product.product', ondelete="cascade")
    price_unit = fields.Float(
        string='Unit Price', required=True, digits='Product Price', related='product_id.list_price',
        compute="_compute_price_unit", readonly=False, store=True)

    product_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True,
                               compute='_compute_product_qty', store=True, readonly=False)
    tax_incl = fields.Monetary(string='Tax Incl', compute='_compute_price_total', currency_field='currency_id')
    taxes_id = fields.Many2many('account.tax', string='Taxes')
    discount_type = fields.Selection([('percentage', 'Percentage'), ('fixed', 'Fixed')], string='Disc Type',
                                     default='percentage')
    discount = fields.Float(string='Disc', digits='Discount')
    currency_id = fields.Many2one('res.currency', related='purchase_id.currency_id')
    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_price_subtotal', currency_field='currency_id')

    # discounted_amount = fields.Monetary(string='Discounted_Amount', compute='_compute_discounted_amount', store=True)
    # amount_tax = fields.Monetary(compute='_compute_new_field', store=True)
    # after_tax = fields.Float(string='after tax')


        # def _compute_discounted_amount(self, original_amount, discount_percentage):
        #     discounted_amount = original_amount * (1 - discount_percentage / 100)
        #     return discounted_amount

    #
    # @api.depends('price_unit','', 'discount_type', 'discount')
    # def _compute_discounted_amount(self):
    #     for line in self:
    #         if line.discount > 0.0:
    #             if line.discount_type == 'percentage':
    #                 total = line.price_unit * line.product_qty
    #                 discount_amount = total * (line.discount or 0.0) / 100.0
    #                 line.discounted_amount = total - discount_amount
    #             elif line.discount_type == 'fixed':
    #                 total = line.price_unit * line.product_qty
    #                 line.discounted_amount = total - (line.discount or 0.0)
    #         else:
    #             line.discounted_amount = 0.0

    @api.depends('price_subtotal', 'taxes_id')
    def _compute_price_total(self):
        for rec in self:
            rec.tax_incl = rec.price_subtotal + sum(rec.taxes_id.mapped('amount'))

    @api.depends('price_unit', 'product_qty')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = (rec.price_unit * rec.product_qty)









    #
    # @api.depends('taxes_id', 'price_subtotal')
    # def _compute_total_with_taxes(self):
    #     """
    #     Compute the total amount including taxes.
    #     """
    #     for order in self:
    #         price_subtotal = order.price_subtotal
    #         for tax in order.taxes_id:
    #             price_subtotal += (price_subtotal * tax.amount / 100)
    #         order.total_with_taxes = price_subtotal


