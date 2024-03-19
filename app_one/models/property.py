from odoo import models,fields,api
from odoo.exceptions import ValidationError
from datetime import timedelta




class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    # this is field to do sequence for property, should this field ref before name
    ref = fields.Char(default="New", readonly=0 )
    name = fields.Char(required=True, size=50, default="New")
    description = fields.Text(tracking=1)
    post_code = fields.Char(required=1)
    date_availability = fields.Date(default=fields.Date.today(),tracking=1)

    expected_price = fields.Float()
    selling_price = fields.Float()

    # this is field to do automated action (date , is_late)
    expected_selling_price_date = fields.Date(tracking=1)
    is_late = fields.Boolean()

    diff = fields.Float(compute='_compute_diff', store=1)

    bedrooms = fields.Integer(required=True)

    living_area = fields.Integer()

    facades = fields.Integer()

    garage = fields.Boolean()

    garden = fields.Boolean()

    garden_area = fields.Integer()

    garden_orientation = fields.Selection([
        ('north', 'north'),
        ('south', 'south'),
        ('east', 'east'),
        ('west', 'west'),

    ], default='north')

    # this is relation with  is called owner and  Ido related field
    owner_id = fields.Many2one('owner')
    owner_address = fields.Char(related='owner_id.address', readonly=0)
    owner_phone = fields.Char(related='owner_id.phone', readonly=0)
    create_time = fields.Datetime(default=fields.Datetime.now())
    next_time = fields.Datetime(compute='_compute_next_time')

    tag_ids = fields.Many2many('tag')

    # this is work flow field state
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'pending'),
        ('sold', 'sold'),
        ('closed', 'Closed'),
        # when you do server action you should select is called (closed) because this is for server action

    ], default='draft')

    active = fields.Boolean(default='true',string='active')
    line_ids = fields.One2many('property.line', 'property_id')

    # this method of validation  constrains
    _sql_constraints = [

        ('name_unique', 'unique("name")', "this name is exist!"),
    ]

    # compute field next_time
    @api.depends('create_time')
    def _compute_next_time(self):
        for rec in self:
            if rec.create_time:
                rec.next_time = rec.create_time + timedelta(hours=6)
            else:
                rec.next_time = False

    @api.depends('expected_price', 'selling_price','owner_id.phone')
    def _compute_diff(self):
        for rec in self :
            rec.diff = rec.expected_price - rec.selling_price

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            print(' inside _onchange_expected_price method')
            return {
                'warning': {
                    'title': "warning",
                    'message': "The number of available  may not be negative",
                    'type': 'notification'
                },
            }

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError("Please add valid number  of bedrooms!")

    # this method of Crud:create,read= search,update=write ,delete=unlink
    @api.model_create_multi
    def create(self,vals):
        rec = super(Property,self).create(vals)
        print("inside create method")
        return rec

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        rec = super(Property , self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
        print("inside search method")
        return rec

    def write(self,vals):
        rec = super(Property,self).write(vals)
        print("inside write method")
        return rec

    def unlink(self):
        rec = super(Property, self).unlink()
        print("inside unlink method")
        return rec



 # this method of workflow field state

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft')
            rec.state = 'draft'


    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending')
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.state = 'sold'

 # this method of server action
    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'

 # this method of automated action
    def check_expected_selling_price_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_price_date and rec.expected_selling_price_date < fields.date.today():
                rec.is_late = True


 # this method of env to do search domain and create inside any mmodel in ui odoo
    def action(self):
        # search domain 1
        print(self.env['property'].search([('name', '=', 'New4')]))

        #  # search domain 2 tuple:
        # print(self.env['property'].search([('name', '=', 'New4'), ('Post Code', '!=', '4')]))
        #
        # # search domain for logical operator(oR | , AND & , NOT !):
        # print(self.env['property'].search(['|', ('name', '=', 'New4'), ('Post Code', '!=', '4')]))
        # print(self.env['property'].search(['&', ('name', '=', 'New4'), ('Post Code', '!=', '4')]))
        # print(self.env['property'].search(['!', ('name', '=', 'New4'), ('Post Code', '!=', '4')]))
        #

        #
        # print(self.env['owner'].create({
        #     'name': '',
        #     'phone': '',
        #     'address': '',
        #     'description': '',
        # }))
        # print(self.env['owner'].search([(
        #     'name', '=', 'mahmoud',)]).unlink())

# this method of sequence field ref
    @api.model
    def create(self, vals):
        rec = super(Property, self).create(vals)
        if rec.ref == 'New':
            rec.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return rec

    # this method to change value of state in this model .its will register automatic in property_history
    def create_history_record(self, old_state, new_state, reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
                'line_ids': [(0, 0, {'description': line.description, 'area': line.area})for line in rec.line_ids],
            })

    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.property_change_state_wizard_action')
        action['context'] = {'default_property_id': self.id}
        return action


    # this method smart button ( method , button in form view with related field)
    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action




# this is class of notebook of property
class PropertyLine(models.Model):
    _name = 'property.line'


    area = fields.Integer()
    description = fields.Char()

    property_id = fields.Many2one('property')




