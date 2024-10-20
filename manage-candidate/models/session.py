# By Atman Boulaajaili
# https://github.com/elon-fask

from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError


class SessionCandidate(models.Model):
    _name = "mo.session.candidate"
    _description = "Manage Session Candidate"

    session_id = fields.Many2one("mo.session", "Session", required=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("done", "Ongoing"),
            ("cancel", "Upcoming"),
        ],
        string="Status",
        default="draft",
    )


class Session(models.Model):
    _name = "mo.session"
    _description = "manage session"
    _inherits = {"res.partner": "partner_id"}

    partner_id = fields.Many2one("res.partner", "Partner")
    session_name = fields.Char(string="Session Name")
    session_number = fields.Char(string="Session Number")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    evaluation_type = fields.Selection(
        [("practical", "Practical"), ("written", "Written")],
        "Evaluation Type",
        required=True,
    )
    school = fields.Selection(
        [("acs", "ACS"), ("ccs", "CCS")],
        string="School",
        required=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("done", "Ongoing"),
            ("cancel", "Upcoming"),
        ],
        string="Status",
        default="draft",
    )
    evaluation_date = fields.Date(string="Evaluation Date")
    registration_close_date = fields.Date(string="Registration Close Date")
    max_unit_load = fields.Float(string="Maximum Unit Load")
    min_unit_load = fields.Float(string="Minimum Unit Load")

    test_site_location = fields.Selection(
        [("site1", "Site 1"), ("site2", "Site 2")],
        string="Test Site Location",
        required=False,
    )
    test_site_address = fields.Char(string="Test Site Address")
    test_site_city = fields.Char(string="City")
    test_site_state = fields.Char(string="State")
    test_site_zip = fields.Char(string="ZIP")

    enrollment_type = fields.Selection(
        [("public", "Public"), ("private", "Private")],
        string="Enrollment Type",
        required=True,
    )
    nccco_fee_note = fields.Text(string="NCCCO Fee Note")
    number_of_candidates = fields.Integer("Number of Candidate")
    assigned_staff = fields.Selection(
        [("staff1", "Antonio Chan"), ("staff2", "Rafael Guzman")],
        string="Assigned Staff",
        required=True,
    )
    test_site_coordinator = fields.Selection(
        selection=[("site_coordinator1", "Jessica Amick")],
        string="Test Site Coordinator",
        required=True,
    )
    # pending_transactions = fields.Integer("Pending Transactions")
    materials_status = fields.Boolean("Materials Status", default=False)

    start_date = fields.Datetime(string="Start Date", required=True)
    end_date = fields.Datetime(string="End Date", required=True)
    # capacity = fields.Integer(string="Capacity")
    # empty_place = fields.Integer(string="Empty Place")
    session_candidate_details_ids = fields.One2many(
        "mo.candidate", "partner_id", string="Session Candidate Details"
    )
    active = fields.Boolean(default=True)

    parent_id = fields.Many2one("mo.session", string="Session Parent")

    @api.constrains("parent_id")
    def _check_parent_id_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_("You cannot create recursive Session."))
        return True
