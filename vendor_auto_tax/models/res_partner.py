from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_default_purchase_tax_id = fields.Many2one(
        'account.tax',
        string='Default Purchase Tax',
        domain="[('type_tax_use', '=', 'purchase')]",
        help="This tax will be automatically applied to purchase order lines for this vendor."
    )
