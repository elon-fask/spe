# Atman Boulaajaili
# https://github.com/elon-fask


from locale import currency
from odoo import models, fields, api, tools, _


class Application(models.Model):
    _name = "mo.application"
    _description = "Manage Application"

    application_name = fields.Char("Application Name", required=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("valid", "Valid"),
            ("archive", "Archive"),
        ],
        default="valid",
        string="Status",
    )
    application_keyword = fields.Char("Keyword", required=True)
    application_description = fields.Text("Description")

    latefee = fields.Monetary("Late Fee", required=True, currency_field="currency_id")
    iaifee = fields.Monetary("IAI Fee", required=True, currency_field="currency_id")
    application_price = fields.Monetary(
        "Price", required=True, currency_field="currency_id"
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )
