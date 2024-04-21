import random
from odoo import api, fields, models
from datetime import datetime, date
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'ref'

    patient_id = fields.Many2one('hospital.patient')
    patient_phone = fields.Char(related='patient_id.phone', tracking=1)
    patient_email = fields.Char(related='patient_id.email', string='Email', tracking=1, default=False)
    gender = fields.Selection(related='patient_id.gender')
    age = fields.Integer(related='patient_id.age')
    ref = fields.Char(string='Reference', related='patient_id.ref')
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    # to calculate duration you should create start date and end date and compute duration to calculate them
    # because you will use it in calendar
    booking_date = fields.Datetime(string='Booking Date', default=fields.Datetime.now)
    appointment_start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    duration = fields.Char(string='Duration', compute="_compute_duration")

    # booking_date = fields.Date(string='Booking Date', default=fields.Datetime.today)
    line_ids = fields.One2many('appointment.line', 'appointment_id', ondelete="cascade")
    amount = fields.Float(string='Amount')
    total_amount = fields.Float('Total Amount', compute='_compute_total_amount',store=1)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')
    ], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ], default='draft', tracking=1, string="status")

    doctor_id = fields.Many2one('res.users', string='Doctor')
    hide_sale_price = fields.Boolean(string='Hide Sale Price')
    # this is field for field monetary
    company_id = fields.Many2one('res.company',string='Company',default=lambda self:self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    # active = fields.Boolean(string='Archived',default='true') this is the best after that
    active = fields.Boolean(string='Archived')
    # this field to create progress and method under you should put it in tree view
    progress = fields.Integer(string='Progress', compute="_compute_progress")

    @api.model
    # this method to send mail betaa3 apoointment_email_template and her button in form view
    def action_send_mail(self):
        # in ref u put (name of your app . id) this id betaa3 appointment_email_template
        template_id = self.env.ref('om_hospital.appointment_email_template').id
        print('hiiiiiiiiiiiiiiiiiiiiiiiiii', template_id)

        template = self.env['mail.template'].browse(template_id)
        print('hiiiiiiiiiiiiiiiiiiiiiiiiii', template)
        # template = self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)
        # for rec in self:
            # print('hiiiiiiiiiiiiiiiiiiiiiiiiii')
            # if rec.patient_id.email:
            #     template.send_mail(rec.id, force_send=True)

 # amount this meaning مبلغ and total amount = all (1+مبلغ+مبلغ 2+مبلغ 3+مبلغ 4)
 #    but in this model found one field for مبلغ it is amount
    @api.depends('amount')
    def _compute_total_amount(self):
        self.total_amount = self.amount
        # self.total_amount = sum(self.mapped('amount')) + self.مبلغ1 + self.مبلغ2


    @api.onchange('patient_id')
    def onchange_patient_id(self):
        for rec in self:
            rec.ref = rec.patient_id.ref

    # this method of sequence ref
    @api.model_create_multi
    def create(self, vals):
        rec = super(HospitalAppointment, self).create(vals)
        if rec.ref == 'New':
            rec.ref = self.env['ir.sequence'].next_by_code('hospital.appointment_seq')
        return rec

    # this method when i delete record state = done from form  inside odoo appear this message
    def unlink(self):
        print("inside unlink method")
        if self.state == 'done':
            raise ValidationError(" you cannot delete 'state in done'")
        return super(HospitalAppointment, self).unlink()
    #
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     rec = super(HospitalAppointment, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #     print("inside search method")
    #     return rec
    #
    # def write(self, vals):
    #     rec = super(HospitalAppointment, self).write(vals)
    #     print("inside write method")
    #     return rec
    #
    # def unlink(self):
    #     rec = super(HospitalAppointment, self).unlink()
    #     print("inside unlink method")
    #     return rec
 # this method of field duration to calculate el modda el zamanyia betwwen end date and start date
 #    this is the best
    @api.depends("booking_date", "end_date")
    def _compute_duration(self):
        for record in self:
            if record.booking_date and record.end_date:
                # you should make end date - start date
                delta = record.end_date - record.booking_date
                record.duration = delta.days
            else:
                record.duration = 0.0

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_in_consultation(self):
        for rec in self:
            rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
    # this is method to make button cancel appear wizard for appointment you put name of your app elly howwa om_hospital and id betaa3 wizard action
    # your app.id wizard action like this ('om_hospital.cancel_appointment_action')
    def action_cancel(self):
        action = self.env.ref('om_hospital.cancel_appointment_action').read()[0]
        return action


    def action(self):
        print(' hi ')
        return {
            'effect': {
                'fadeout': 'fast',
                'message': 'Click Successfull',
                'type': 'rainbow_man',
            }
        }

    def action_test(self):
        print(' yes, i sure execute python code')
        # you put  return under any method if you want to appear the shape coas kazah men
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Click Successfull',
                'type': 'rainbow_man',
            }
        }


    # this method to do integration with whatsapp but but el model elly feeh name and phone you should do relation field with it Many2one
    def action_share_whatsapp(self):
        if not self.patient_id.phone:
            raise ValidationError(" Missing Phone Number ")
        # you did related field with model patient in ref
        # message = 'Hi *%s*, you *appointment* number is: %s, Thank You ' % (self.patient_id.name,self.ref)
        # even if do related you do self.patient_id.ref because patient has ref field
        # message = 'Hi *%s*, you *appointment* number is: %s, Thank You ' % (self.patient_id.name,self.patient_id.ref)
        message = ' *this integration odoo with whatsapp*  {}, Thank You ' .format(self.patient_id.name)
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.patient_id.phone, message)
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url,
        }

        # this method of automated action on field email = false to make it true
    # def test_cron_job(self):
    #     print('hhhhhhhhhhhhhhhh')
    #     appointment_ids = self.env['hospital.appointment'].search(['patient_phone', '=', True])
    #     for rec in appointment_ids:
    #         if rec.patient_phone:
    #             rec.test_cron_job()
    #             rec.action_share_whatsapp()

    # this method smart button ( method , button in form view with related field)
    def action_open_related_patient(self):

        # om_hospital.patient_action this is id betaa3  act_action_window betaa3 model patient
        action = self.env['ir.actions.actions']._for_xml_id('om_hospital.patient_action')
        # and this is betaa3 form view betaa3 model patient  view_id = self.env.ref('om_hospital.hospital_patient_view_form').id
        # om_hospital.hospital_patient_view_form this is el id betaa3 formview bbetaaa3 model patient
        view_id = self.env.ref('om_hospital.hospital_patient_view_form').id
        # it want el id from relation field patient_id.id
        action['res_id'] = self.patient_id.id
        action['views'] = [[view_id, 'form']]
        return action

     # this method progress  this field  progress = fields.Integer(string='Progress', compute="_compute_progress")
    # and put it in tree view with widget = progressbar , and you should put it in notebok like this
    # <page string="Progress" name="progress">
    #      <field name="progress" widget = 'gauge'/>
    # </page>
    # notice: you put widget in tree view widget = progressbar like this  <field name="progress" widget = 'progressbar'/>
    # but you put widget in notebok widget = gauge like this    <field name="progress" widget = 'gauge'/>
    # to use randomrange you should import random firstly and use it in method progress like this progress = random.randrange(0, 25)

    @api.depends("state")
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                # progress = 25 or random.randrange(0, 25) but random.randrange is best
                progress = random.randrange(0, 25)
            elif rec.state == 'in_consultation':
                # progress = 50
                progress = random.randrange(25, 99)
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress






class AppointmentLine(models.Model):
    _name = 'appointment.line'

    appointment_id = fields.Many2one('hospital.appointment', ondelete="cascade")
    prescription = fields.Html()
    description = fields.Char()
    price_unit = fields.Float(string='Price')
    quantity = fields.Integer(string='Quantity')
    # to create field monetary to calculate depit - credit and then put field monetary in notebook
    currency_id = fields.Many2one('res.currency', related='appointment_id.currency_id')
    price_subtotal = fields.Monetary(string='Subtotal',compute='_compute_price_subtotal', currency_field='currency_id')

    @api.depends('price_unit', 'quantity')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.quantity

