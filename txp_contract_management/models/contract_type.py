from odoo import models, fields

class ContractType(models.Model):
    _name = 'contract.type'
    _description = 'Contract Category / Type'

    name = fields.Char(string='Type Name', required=True)
    code = fields.Char(string='Code')
    color = fields.Integer(string='Color Index')