from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class OpApplication(models.Model):
    
    _name = "op.application"
    _description = "Application Management"
    
    application_name = fields.Char("Application Name", required=True)
    keyword = fields.Char("Keyword")
    application_description = fields.Text("Description")
    application_price = fields.Monetary("Price", currency_field="currency_id")
    nccco_testing_service_fee = fields.Monetary("NCCCO TESTING SERVICE FEE", currency_field="currency_id")
    late_fee = fields.Monetary("Late fee", currency_field="currency_id")
    application_status = fields.Selection([("public", "Public"), ("private", "Private"), ("archive", "Archive")])
    
    
    
    currency_id = fields.Many2one("res.currency", string="Currency")
    
    
    
    
    
    