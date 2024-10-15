# BY Atman Boulaajaili
# https://github.com/elon-fask

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging


_logger = logging.getLogger(__name__)

class OpCourse(models.Model):
    _name = "op.course"
    _inherit = "mail.thread"
    _description = "Course Model"

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', size=16, required=True)
    parent_id = fields.Many2one('op.course', 'Parent Course')
    evaluation_type = fields.Selection(
        [('normal', 'Normal'), ('test1', 'test1'),
         ('test2', 'test2'), ('test3', 'test3')],
        'Evaluation Type', default="normal", required=True)
    # subject_ids = fields.Many2many('op.subject', string='Subject(s)')
    # max_unit_load = fields.Float("Maximum Unit Load")
    # min_unit_load = fields.Float("Minimum Unit Load")
    # department_id = fields.Many2one(
    #     'op.department', 'Department',
    #     default=lambda self:
    #     self.env.user.dept_id and self.env.user.dept_id.id or False)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_course_code',
         'unique(code)', 'Code should be unique per course!')]

    @api.constrains('parent_id')
    def _check_parent_id_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive Course.'))
        return True

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Courses'),
            'template': '/manage-students/static/xls/op_course.xls'
        }]