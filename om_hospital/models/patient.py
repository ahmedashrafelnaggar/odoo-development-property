from odoo import api, fields, models
from datetime import datetime, date
from odoo.exceptions import ValidationError



class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(string='Reference', default='New', tracking=1)
    name = fields.Char(string='Name', tracking=1)
    phone = fields.Char(string='Phone', tracking=1)
    email = fields.Char(string='Email', tracking=1,default=False)
    # i will do relation field many2 one  with  doctor.py nmaemodel hospital.doctor this mean i want to appear this model here
    doctor_id = fields.Many2one('hospital.doctor' , string='Doctor')
    date_of_birth = fields.Date(string='Date Of Birth', default=fields.Datetime.now())
    age = fields.Integer(string='Age', tracking=1, compute='compute_age', store=1)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], default='male', string="Gender", tracking=1)

    lang = fields.Selection([
        ('arabic', 'Arabic'),
        ('english', 'English'),
    ], default='arabic', string="Language", tracking=1)
    parent = fields.Char(string='Parent', tracking=1)
    active = fields.Boolean(string='Active', default=True)
    appointment_id = fields.Many2one('hospital.appointment', onedelete='restrict')
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')
    user_id = fields.Many2one('res.users', string='Doctor')
    line_ids = fields.One2many('patient.line', 'patient_id',ondelete="cascade")
    image = fields.Binary()
    amount = fields.Float(string='Amount')
    sno = fields.Integer(string='SNO', compute='_compute_sno')
    tad_ids = fields.Many2many('patient.tag', string='Tags')
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count', store=1)
    marital_status = fields.Selection([
        ('married', 'Married'),
        ('single', 'Single'),
    ], default='married', string="Marital Status", tracking=1)
    partner_name = fields.Char(string='Partner Name', tracking=1)





    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            if rec.appointment_ids:
                # you tell him search in model hospital.appointment about record patient_id  which is in model hospital appointment = id in hospital patient
                # meaning you make appointment_count == id in another model but you need firstly connect between model appointment and patient throw
                # many2noe in two models then you want to make appointment_count == id beta3 field patient_id elly mawgood inside this model hospital.appointment
                rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

     # this method when you check model appointment inside model patient you should first do relation one2many
    # this method not make  you delete any method for model appointment inside patient
    # this when you do delete for any data in model inside odoo not do delete because you used ondelete uninstall=false
    @api.ondelete(at_uninstall=False)
    def check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError('you cannot delete patient with appointments')


    @api.depends('date_of_birth')
    def compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 1

    # this method of sequence ref
    @api.model_create_multi
    def create(self, vals):
        rec = super(HospitalPatient, self).create(vals)
        if rec.ref == 'New':
            rec.ref = self.env['ir.sequence'].next_by_code('hospital.patient_seq')
        return rec

    @api.model
    def write(self, vals):
        # super(HospitalPatient, self).write(vals)
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient_seq')
        return super(HospitalPatient, self).write(vals)

    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        rec = super(HospitalPatient, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
        print("inside search method")
        return rec

    def unlink(self):
        rec = super(HospitalPatient, self).unlink()
        print("inside unlink method")
        return rec

    # this method to get ref + name
    @api.model
    def name_get(self):
        return [(record.id, '[{}] {}' .format(record.id, record.name))for record in self]

    # this method to get ref + name another way
    # @api.model
    # def name_get(self):
    #     result = []
    #     for record in self:
    #         display_name = "[{}] {}".format(record.id, record.name)
    #         result.append((record.id, display_name))
    #     return result




    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            # this meaning if this record exit and > from the date today appear this message
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError("not acceptable!")


    # this method because i want to do serial number so that i create field called sno and this is compute for it to make every patient have sequence and serial number
    @api.depends('name')
    def _compute_sno(self):
        for rec in self:
            sno = rec.id
            rec.sno = sno

      # this method to do integratio with whatsapp i did it in model hospital.appointment
    def action_share_whatsapp(self):
        return
    # i write it in model appointment

    # this method of automated action on field email = false to make it true
    def test_cron_job(self):
        appointment_ids = self.env['hospital.appointment'].search(['email', '=', False])
        for rec in appointment_ids:
            if rec.email is False:
                rec.test_cron_job()
                rec.email = True
    #             # you say if method beta3 email if false you make it true








class PatientLine(models.Model):
    _name = 'patient.line'

    patient_id = fields.Many2one('hospital.patient', ondelete="cascade")
    prescription = fields.Html()

    description = fields.Char()