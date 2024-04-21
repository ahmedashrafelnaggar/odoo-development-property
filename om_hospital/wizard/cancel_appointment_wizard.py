from odoo import api, fields, models
from odoo.exceptions import ValidationError
import datetime


class CancelAppointment(models.TransientModel):
    _name = "cancel.appointment"
    _description = "Cancel Appointment"

     # when you put domain this meaning condithion appear all which contain on state = draft only you are choice put domain in logic tier or presentation tier
    # and you should do relation field Many2one with model elly you want wizzard appear in it so i want my wizzard appear in model hospital.appointment
    # and method here for action_cancel_appointment and method in model hospital.appointment for action_cancel to connect them with some
    # and you do button here.xml for method action_cancel_appointment in footer and button in hospital.appointment and put it in form view name of method action_cancel
    # then you connect between button action_cancel when i press on it open wizard this result you make in button in model hospital.appointment type=actio , name = name of your app.id betaa3 action wizard
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment', domain=[('state', '=', 'done')])
    reason = fields.Text()
    cancel_date = fields.Date(string='Cancellation Date')

    # this is method to get_default to anything like time automatic, because i want to get today for record cancel_date
    # and if i want get any thing for any record write like this res['record_name'] = write here what you want
    @api.model
    def default_get(self, fields):
        res = super(CancelAppointment, self).default_get(fields)
        res['cancel_date'] = datetime.date.today()
        # i can get active_id from method and from put attribute name it context under button cancel , because it appear wizard
        # res['appointment_id'] = self.env.context.get('active_id')
        # this too if i want get the reason by automatic or default
        # res['reason'] = self.env.context.get('test')
        return res

    # this is button when you press on it appear the cancel_appointment_wizard to tell the patient No booking_date in the same today
    def action_cancel_appointment(self):
        for rec in self:
            if rec.appointment_id.booking_date == fields.Date.today():
                raise ValidationError("sorry, cancellation is not allowed on the same day of booking!")
            # you should write this field appointment_id.state ='cancel' because when you press button cancel it make delete
            rec.appointment_id.state = 'cancel'
            return

