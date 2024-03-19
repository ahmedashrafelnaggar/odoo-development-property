from odoo import models ,fields,api
from datetime import timedelta



class TodoTask(models.Model):
    _name = 'todo.task'
    _rec_name='name'
    _description = 'TodoTask'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string='Task Name')
    due_date = fields.Date(default=fields.Date.today())
    description = fields.Text()
    assign_to_id = fields.Many2one('res.partner')
    active = fields.Boolean(default=True,string='active')

    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In_Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),

    ], default='new')

    line_ids = fields.One2many('todo_task.line', 'todo_task_id')


    @api.model_create_multi
    def create(self, vals):
        rec = super(TodoTask, self).create(vals)
        print("inside create method")

        return rec

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        rec = super(TodoTask, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
        print("inside search method")
        return rec

    def write(self, vals):
        rec = super(TodoTask, self).write(vals)
        print("inside write method")
        return rec

    def unlink(self):
        rec = super(TodoTask, self).unlink()
        print("inside unlink method")
        return rec

    def action_new(self):
        for rec in self:
            rec.state = 'new'

    def action_in_progress(self):
        for rec in self:
            rec.state = 'in_progress'

    def action_completed(self):
        for rec in self:
            print(" inside in completed ")
            rec.state = 'completed'

    def action_closed(self):
        for rec in self:
            rec.state = 'closed'


class TodoTaskLine(models.Model):
    _name ='todo_task.line'




    Date = fields.Date(default=fields.Date.today())
    description = fields.Char()
    Time = fields.Float(string='Time')



    todo_task_id = fields.Many2one('todo.task')


