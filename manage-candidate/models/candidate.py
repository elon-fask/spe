# Atman Boulaajaili
# https://github.com/elon-fask


from locale import currency
from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError


class CandidateApplicationLine(models.Model):
    _name = "mo.candidate.application.line"
    _description = "Manage Candidate Application Line"
    _rec_name = "candidate_id"

    candidate_id = fields.Many2one(
        "mo.candidate", "Candidate", ondelete="cascade", tracking=True
    )
    application_id = fields.Many2one(
        "mo.application",
        "Application",
        required=True,
        tracking=True,
        store=True,
        # domain=[("state", "=", "valid")],
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("valid", "Valid"),
            ("archive", "Archived"),
        ],
        string="Status",
        default="valid",
    )
    # Related fields from mo.application
    application_name = fields.Char(
        related="application_id.application_name", string="Application Name", store=True
    )
    application_price = fields.Monetary(
        related="application_id.application_price", string="Price", store=True
    )
    latefee = fields.Monetary(
        related="application_id.latefee", string="Late Fee", store=True
    )
    iaifee = fields.Monetary(
        related="application_id.iaifee", string="IAI Fee", store=True
    )
    currency_id = fields.Many2one(
        related="application_id.currency_id", string="Currency", store=True
    )


class CandidateSession(models.Model):
    _name = "mo.candidate.session"
    _description = "Manage Candidate Session"
    _inherit = "mail.thread"
    _rec_name = "candidate_id"

    candidate_id = fields.Many2one(
        "mo.candidate", "Candidate", ondelete="cascade", tracking=True,store=True
    )
    session_id = fields.Many2one("mo.session", "Session",stor=True, required=True, tracking=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("done", "Ongoing"),
            ("cancel", "Upcoming"),
        ],
        string="Status",
        default="done",
    )
    start_date = fields.Date("Start Date", tracking=True)
    end_date = fields.Date("End Date", tracking=True)


class Candidate(models.Model):
    _name = "mo.candidate"
    _description = "Manage Candidate"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _inherits = {"res.partner": "partner_id"}

    first_name = fields.Char("First Name")
    middle_name = fields.Char("Middle Name")
    last_name = fields.Char("Last Name")
    birth_date = fields.Date("Birth Date")
    nationality = fields.Many2one("res.country", "Nationality")
    # emergency_contact = fields.Many2one("res.partner", "Emergency Contact")
    id_number = fields.Char("ID Card Number", size=64)
    partner_id = fields.Many2one(
        "res.partner", "Partner", required=False, ondelete="cascade"
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("done", "Done"),
            ("cancel", "Cancel"),
            ("pending", "Pending"),
            ("rejected", "Rejected"),
            ("running", "Running"),
        ],
        string="Status",
        default="running",
    )
    gr_no = fields.Char("Registration Number", size=20)

    # session_details_ids = fields.One2many(
    #     "mo.candidate.session", "candidate_id", "Session Details"
    # )
    session_details_ids = fields.One2many(
        "mo.candidate.session", "candidate_id", "Session Details", store=True, required=True
    )

    application_line_ids = fields.One2many(
        "mo.candidate.application.line", "candidate_id", "Application Line", store=True, required=True
    )
    gender = fields.Selection(
        [("m", "Male"), ("f", "Female"), ("o", "Other")],
        "Gender",
        required=True,
        default="m",
    )
    company_name = fields.Char("Company Name")
    contact_name = fields.Char("Contact Name")
    contact_email = fields.Char("Contact Email")
    company_address = fields.Char("Company Address")
    company_city = fields.Char("Company City")
    company_state = fields.Char("Company State")
    company_zip = fields.Char("Company Zip")
    mobile = fields.Char("Mobile")
    email = fields.Char("Email")
    is_purchase_order = fields.Boolean("Is Purchase Order", default=False)
    amount_owed = fields.Monetary("Amount Owed", currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Currency")
    image_1920 = fields.Image(string="Candidate Image", max_width=1920, max_height=1920)
    cco_id = fields.Char("CCO ID", required=True)
    cco_certification_number = fields.Char("CCO Certification Number")
    user_id = fields.Many2one("res.users", "User")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("gr_no_uniq", "unique(gr_no)", "The Registration Number must be unique!"),
    ]

    # @api.onchange('first_name', 'middle_name', 'last_name')
    #     def _onchange_name(self):
    #         if not self.middle_name:
    #             self.name = str(self.first_name) + " " + str(
    #                 self.last_name
    #             )
    #         else:
    #             self.name = str(self.first_name) + " " + str(
    #                 self.middle_name) + " " + str(self.last_name)

    @api.onchange("first_name", "middle_name", "last_name")
    def _onchange_name(self):
        if not self.middle_name:
            self.name = str(self.first_name) + " " + str(self.last_name)
        else:
            self.name = (
                str(self.first_name)
                + " "
                + str(self.middle_name)
                + " "
                + str(self.last_name)
            )

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

    def create_candidate_user(self):
        user_group = self.env.ref("base.group_portal") or False
        users_res = self.env["res.users"]
        for record in self:
            if not record.user_id:
                user_id = users_res.create(
                    {
                        "name": record.name,
                        "partner_id": record.partner_id.id,
                        "login": record.email,
                        "groups_id": user_group,
                        "tz": self._context.get("tz"),
                    }
                )
                record.user_id = user_id
