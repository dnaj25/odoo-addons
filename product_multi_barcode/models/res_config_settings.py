from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_product_multi_barcode_uniq = fields.Boolean(
        string="Unique Extra Barcode Verification",
        config_parameter='product_multi_barcode.uniq_barcode',
        help="Enforce unique validation on extra product barcodes."
    )
