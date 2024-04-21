from odoo import api, fields, models
from datetime import datetime, date


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctor"
    _inherit = ['mail.thread','mail.activity.mixin']

    ref = fields.Char(string='Reference', tracking=1, default='Odoo Mates')
    doctor_name = fields.Char(string='Name', tracking=1)
    note = fields.Text(string='Note', tracking=1)
    date_of_birth = fields.Date(string='Date Of Birth')
    age = fields.Integer(string='Age', tracking=1, compute='compute_age', store=1)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], default='male', string="Gender", tracking=1)
    active = fields.Boolean(string='Active', default=True)
    doctor_id = fields.Many2one('res.users', string='Doctor')
    line_ids = fields.One2many('patient.line', 'patient_id', ondelete="cascade")

    @api.depends('date_of_birth')
    def compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 1


class DoctorLine(models.Model):
    _name = 'doctor.line'

    doctor_id = fields.Many2one('hospital.doctor', ondelete="cascade")
    prescription = fields.Html()
    description = fields.Char()

