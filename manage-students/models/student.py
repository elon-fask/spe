# By Atman Boulaajaili
# https://github.com/elon-fask

from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError
import logging


class OpStudentCourse(models.Model):
    _name = "op.student.course"
    _description = "Student Details"
    _inherit = "mail.thread"
    _rec_name = "student_id"

    student_id = fields.Many2one(
        "op.student", "Student", ondelete="cascade", tracking=True
    )
    course_id = fields.Many2one("op.course", "Course", required=True, tracking=True)
    # batch_id = fields.Many2one("op.batch", "Batch", required=True, tracking=True)
    roll_number = fields.Char("Roll Number", tracking=True)
    # subject_ids = fields.Many2many("op.subject", string="Subjects")
    # academic_years_id = fields.Many2one("op.academic.year", "Academic Year")
    # academic_term_id = fields.Many2one("op.academic.term", "Terms")
    state = fields.Selection(
        [("Draft", "Draft"), ("running", "Running"), ("finished", "Finished")],
        string="Status",
        default="running",
    )

    _sql_constraints = [
        (
            "unique_name_roll_number_id",
            # "unique(roll_number,course_id,batch_id,student_id)",
            # "Roll Number & Student must be unique per Batch!",
            "unique(roll_number,course_id,student_id",
            "Roll Number & Student must be unique per Batch",
        ),
        (
            "unique_name_roll_number_course_id",
            # "unique(roll_number,course_id,batch_id)",
            "unique(roll_number,course_id)",
            "Roll Number must be unique per Batch!",
        ),
        (
            "unique_name_roll_number_student_id",
            # "unique(student_id,course_id,batch_id)",
            "unique(student_id,course_id)",
            "Students must be unique per batch!",
        ),
    ]

    @api.model
    def get_import_templates(self):
        return [
            {
                "label": _("Import Template for Student Course Details"),
                "template": "/manage-students/static/xls/op_student_course.xls",
            }
        ]


class OpStudent(models.Model):
    _name = "op.student"
    _description = "Student"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    # _inherits = {"res.partner": "partner_id"}

    _logger = logging.getLogger(__name__)

    _logger.info("Loading OpStudent Model")

    # student_id = fields.Integer(string="student id")
    first_name = fields.Char("First Name", translate=True)
    middle_name = fields.Char("Middle Name", translate=True)
    last_name = fields.Char("Last Name", translate=True)
    birth_date = fields.Date("Birth Date")
    gender = fields.Selection(
        [("m", "Male"), ("f", "Female"), ("o", "Other")],
        "Gender",
        required=True,
        default="m",
    )
    mobile = fields.Char("Mobile")
    email = fields.Char("Email")
    image_1920 = fields.Image(string="Student Image", max_width=1920, max_height=1920)
    street = fields.Char("Street")
    city = fields.Char("City")
    zip = fields.Char("Zip")
    id_number = fields.Char("ID Card Number", size=66)
    gr_no = fields.Char("Registration Number", size=20)
    # category_id = fields.Many2one("op.category", "Category")
    # course_detail_ids = fields.One2many(
    #     "op.student.course", "student_id", "Course Details", tracking=True
    # )
    active = fields.Boolean(default=True)

    is_purchase_order = fields.Boolean("Is Purchase Order", default=False)
    amount_owed = fields.Monetary("Amount Owed", currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Currency")
    cco_id = fields.Char("CCO ID", required=True)
    cco_certification_number = fields.Char("CCO Certification Number")

    company_name = fields.Char("Company | Organization")
    company_phone = fields.Char("Company phone")
    company_address = fields.Char("Company Address")
    contact_name = fields.Char("Contact Name")
    contact_email = fields.Char("Contact Email")
    company_state = fields.Char("Company State")
    company_city = fields.Char("Company Cite")
    company_zip = fields.Char("Company ZIP")

    _sql_constraints = [
        (
            "unique_gr_no",
            "unique(gr_no)",
            "Registration Number must be unique per student!",
        )
    ]

    #
    # @api.onchange("first_name", "middle_name", "last_name")
    # def _onchange_name(self):
    #     if not self.middle_name:
    #         self.display_name = str(self.first_name) + " " + str(self.last_name)
    #     else:
    #         self.display_name = (
    #             str(self.first_name)
    #             + " "
    #             + str(self.middle_name)
    #             + " "
    #             + str(self.last_name)
    #         )
    #
    @api.constrains("birth_date")
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(
                    _("Birth Date can't be greater than current date!")
                )

    @api.onchange("email")
    def _validate_email(self):
        if self.email and not tools.single_email_re.match(self.email):
            raise ValidationError(
                _("Invalid Email! Please enter a valid email address.")
            )

    @api.onchange("mobile")
    def _validate_mobile(self):
        if self.mobile and self.mobile.isalpha():
            raise ValidationError(_("Enter Your Valid Mobile Number"))

    @api.model
    def get_import_templates(self):
        return [
            {
                "label": _("Import Template for Students"),
                "template": "/manage-students/static/xls/op_student.xls",
            }
        ]

    # def create_student_user(self):
    #     user_group = self.env.ref("base.group_portal") or False
    #     users_res = self.env["res.users"]
    #     for record in self:
    #         if not record.user_id:
    #             user_id = users_res.create(
    #                 {
    #                     "name": record.name,
    #                     "partner_id": record.partner_id.id,
    #                     "login": record.email,
    #                     "groups_id": user_group,
    #                     "is_student": True,
    #                     "tz": self._context.get("tz"),
    #                 }
    #             )
    #             record.user_id = user_id
