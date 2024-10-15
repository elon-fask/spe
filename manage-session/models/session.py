# By Atman Boulaajaili
# https://github.com/elon-fask
from dataclasses import field
from odoo import models, fields, api


class OpSession(models.Model):
    _description = "Session"
    _name = "op.session"
    
    # session_id = fields.Many2one("op.student", string="session")
    session_name = fields.Char("Session Name", required=True)
    location = fields.Char("Location", required=True)
    number_of_candidates = fields.Integer("Number of Candidate")
    assigned_staff = fields.Selection(
        [("coordinator1", "Antonio Chan"), ("coordinator2", "Rafael Guzman")],
        string="Assigned Staff",
        required = True,
    )
    test_site_coordinator = fields.Selection(selection=[("site_coordinator", "Jessica Amick")], string="Test Site Coordinator", required=True)
    pending_transactions = fields.Integer("Pending Transactions")
    materials_status = fields.Boolean("Materials Status", default=False)
    start_date = fields.Datetime(string="Start Date", required=True)
    end_date = fields.Datetime(string="End Date", required=True)
    capacity = fields.Integer(string="Capacity")
    empty_place = fields.Integer(string="Empty Place")

    student_line = fields.One2many('op.student.line', 'session_id', string='Student Lines')

    active = fields.Boolean(default=True)
