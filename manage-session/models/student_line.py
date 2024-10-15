# By Atman Boulaajaili
# https://github.com/elon-fask

from odoo import models, fields, api


class OpStudentLine(models.Model):
    _name = "op.student.line"
    _description = "Student Details"
    _inherits = {"op.student": "student_id"}

    student_id = fields.Many2one("op.student", string="Student")
    session_id = fields.Many2one("op.session", string="Session")

    # Now you can access fields from the op.student model, such as first_name
    first_name = fields.Char(related="student_id.first_name", string="First Name")
    last_name = fields.Char(related="student_id.last_name", string="Last Name")
