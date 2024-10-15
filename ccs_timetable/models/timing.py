# By Atman Boulaajaili
# https://github.com/elon-fask

from odoo import models, fields

class OpTiming(models.Model):
    _name = "op.timing"
    _description = "Period"

    name = fields.Char("name", size=16, required=True)
    hour = fields.Selection(
        [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"),
         ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10"),
         ("11", "11"), ("12", "12")], "Hours", required=True)
    minute = fields.Selection(
        [("00", "00"), ("15", "15"), ("30", "30"), ("45", "45")], "Minute",
        required=True)
    am_pm = fields.Selection(
        [("am", "AM"), ("pm", "PM")], "AM/PM", required=True)
