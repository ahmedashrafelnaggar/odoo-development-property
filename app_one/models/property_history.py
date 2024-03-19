from odoo import models,fields,api
from odoo.exceptions import ValidationError


class PropertyHistory(models.Model):
    _name = 'property.history'
    _description = 'Property History'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    user_id = fields.Many2one('res.users')
    property_id = fields.Many2one('property')
    old_state = fields.Char()
    new_state = fields.Char()
    reason = fields.Char()
    line_ids = fields.One2many('property.history.line', 'history_id')


class PropertyHistoryLine(models.Model):
    _name = 'property.history.line'

    history_id = fields.Many2one('property.history')
    area = fields.Char()
    description = fields.Text()



#     # this is field to do sequence for property, should this field ref before name
#     ref = fields.Char(default="New", readonly=1)
#     name = fields.Char(required=True, default="New")
#     description = fields.Text(tracking=1)
#     post_code = fields.Char(required=1)
#     date_availability = fields.Date(default=fields.Date.today(),tracking=1)
#
#     expected_price = fields.Float()
#     selling_price = fields.Float()
#
#     # this is field to do automated action (date , is_late)
#     expected_selling_price_date = fields.Date(tracking=1)
#     is_late = fields.Boolean()
#
#     diff = fields.Float(compute='_compute_diff', store=1)
#
#     bedrooms = fields.Integer(required=True)
#
#     living_area = fields.Integer()
#
#     facades = fields.Integer()
#
#     garage = fields.Boolean()
#
#     garden = fields.Boolean()
#
#     garden_area = fields.Integer()
#
#     garden_orientation = fields.Selection([
#         ('north', 'north'),
#         ('south', 'south'),
#         ('east', 'east'),
#         ('west', 'west'),
#
#     ], default='north')
#
#     # this is relation with  is called owner and  Ido related field
#     owner_id = fields.Many2one('owner')
#     owner_address = fields.Char(related='owner_id.address', readonly=0)
#     owner_phone = fields.Char(related='owner_id.phone', readonly=0)
#
#     tag_ids = fields.Many2many('tag')
#
#     # this is work flow field state
#     state = fields.Selection([
#         ('draft', 'Draft'),
#         ('pending', 'pending'),
#         ('sold', 'sold'),
#         ('closed', 'Closed'),
#         # when you do server action you should select is called (closed) because this is for server action
#
#     ], default='draft')
#
#     active = fields.Boolean(default='true',string='active')
#     line_ids = fields.One2many('property.line', 'property_id')
#
#     # this method of validation  constrains
#     _sql_constraints = [
#
#         ('name_unique', 'unique("name")', "this name is exist!"),
#     ]
#
#     @api.depends('expected_price', 'selling_price','owner_id.phone')
#     def _compute_diff(self):
#         for rec in self :
#             rec.diff = rec.expected_price - rec.selling_price
#
#     @api.onchange('expected_price')
#     def _onchange_expected_price(self):
#         for rec in self:
#             print(' inside _onchange_expected_price method')
#             return {
#                 'warning': {
#                     'title': "warning",
#                     'message': "The number of available  may not be negative",
#                     'type': 'notification'
#                 },
#             }
#
#     @api.constrains('bedrooms')
#     def _check_bedrooms_greater_zero(self):
#         for rec in self:
#             if rec.bedrooms == 0:
#                 raise ValidationError("Please add valid number  of bedrooms!")
#
#     # this method of Crud:create,read= search,update=write ,delete=unlink
#     @api.model_create_multi
#     def create(self,vals):
#         rec = super(Property,self).create(vals)
#         print("inside create method")
#         return rec
#
#     @api.model
#     def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
#         rec = super(Property , self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
#         print("inside search method")
#         return rec
#
#     def write(self,vals):
#         rec = super(Property,self).write(vals)
#         print("inside write method")
#         return rec
#
#     def unlink(self):
#         rec = super(Property, self).unlink()
#         print("inside unlink method")
#         return rec
#
#
#
#  # this method of workflow field state
#
#     def action_draft(self):
#         for rec in self:
#             rec.state = 'draft'
#
#
#     def action_pending(self):
#         for rec in self:
#             rec.state = 'pending'
#
#     def action_sold(self):
#         for rec in self:
#             print(" inside in sold ")
#             rec.state = 'sold'
#
#
#
#  # this method of server action
#     def action_closed(self):
#         for rec in self:
#             rec.state = 'closed'
#
#  # this method of automated action
#     def  check_expected_selling_price_date(self):
#         property_ids = self.search([])
#         for rec in property_ids:
#             if rec.expected_selling_price_date and rec.expected_selling_price_date < fields.date.today():
#                 rec.is_late = True
#
#  # this method of env
#     def action(self):
#         print(self.env['owner'].create({
#             'name': '',
#             'phone': '',
#             'address': '',
#             'description': '',
#         }))
#         # print(self.env['owner'].search([(
#         #     'name', '=', 'mahmoud',)]).unlink())
#
# # this method of sequence field ref
#     @api.model
#     def create(self, vals):
#         rec = super(Property, self).create(vals)
#         if rec.ref == 'New':
#             rec.ref = self.env['ir.sequence'].next_by_code('property_seq')
#         return rec
#
#
#
# # this is class of notebook of property
# class PropertyLine(models.Model):
#     _name = 'property.line'
#
#
#     area = fields.Integer()
#     description = fields.Char()
#
#     property_id = fields.Many2one('property')
#
#
