# By Atman Boulaajaili
# https://github.com/elon-fask
import calendar
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import pytz


week_days = [
    (calendar.day_name[0], _(calendar.day_name[0])),
    (calendar.day_name[1], _(calendar.day_name[1])),
    (calendar.day_name[2], _(calendar.day_name[2])),
    (calendar.day_name[3], _(calendar.day_name[3])),
    (calendar.day_name[4], _(calendar.day_name[4])),
    (calendar.day_name[5], _(calendar.day_name[5])),
    (calendar.day_name[6], _(calendar.day_name[6])),
]


class OpTimetable(models.Model):
    _name = "op.timetable"
    _inherit = ["mail.thread"]
    _description = "Timetable"

    timing_id = fields.Many2one("op.timing", string="Timing", tracking=True)
    name = fields.Char(compute="_compute_name", string="Name", store=True)
    start_datetime = fields.Datetime(string="Start Time", required=True)
    end_datetime = fields.Datetime(string="End Time", required=True)
    session_id = fields.Many2one("op.session", string="Session", required=True)
    color = fields.Integer(string="Color Index")
    type = fields.Char(compute="_compute_day", string="Day", store=True)
    state = fields.Selection(
        [("draft", "Draft"), ("confirm", "Confirmed"), ("done", "Done"), ("cancel", "Canceled")],
        string="Status", default="draft")
    active = fields.Boolean(default=True)
    days = fields.Selection(
        [
            ("monday", "Monday"),
            ("tuesday", "Tuesday"),
            ("wednesday", "Wednesday"),
            ("thursday", "Thursday"),
            ("friday", "Friday"),
            ("saturday", "Saturday"),
            ("sunday", "Sunday")],
        string="Days", group_expand="_expand_groups", store=True)
    timing = fields.Char(compute="_compute_timing")

    @api.depends("start_datetime", "end_datetime")
    def _compute_timing(self):
        tz = pytz.timezone(self.env.user.tz)
        for session in self:
            session.timing = str(session.start_datetime.astimezone(tz).strftime('%I:%M%p')) + ' - ' + str(session.end_datetime.astimezone(tz).strftime('%I:%M%p'))

    @api.model
    def _expand_groups(self, days, domain, order):
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        return [day for day in weekdays if day in days]

    @api.depends("start_datetime")
    def _compute_day(self):
        days = {0: "monday", 1: "tuesday", 2: "wednesday", 3: "thursday", 4: "friday", 5: "saturday", 6: "sunday"}
        for record in self:
            record.type = days.get(record.start_datetime.weekday()).capitalize()
            record.days = days.get(record.start_datetime.weekday())

    @api.depends("session_id", "start_datetime", "end_datetime")
    def _compute_name(self):
        tz = pytz.timezone(self.env.user.tz)
        for session in self:
            if session.session_id and session.start_datetime and session.end_datetime:
                session.name = session.session_id.session_name + ":" + str(session.start_datetime.astimezone(tz).strftime('%I:%M%p')) + '-' + str(session.end_datetime.astimezone(tz).strftime('%I:%M%p'))

    @api.constrains("start_datetime", "end_datetime")
    def _check_date_time(self):

        if self.start_datetime >= self.end_datetime:
            raise ValidationError(_("End time should be greater than start time"))












