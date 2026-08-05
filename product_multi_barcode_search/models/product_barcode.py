from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ProductBarcode(models.Model):
    _name = 'product.barcode'
    _description = 'Product Extra Barcode'
    _order = 'sequence, id'

    name = fields.Char(string='Barcode', required=True, index=True)
    product_id = fields.Many2one('product.product', string='Product Variant', required=True, ondelete='cascade')
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', related='product_id.product_tmpl_id', store=True, readonly=True)
    sequence = fields.Integer(string='Sequence', default=10)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    @api.constrains('name', 'company_id')
    def _check_barcode_uniqueness(self):
        for rec in self:
            if not rec.name:
                continue
            # Check if uniqueness setting is active
            limit_unique = self.env['ir.config_parameter'].sudo().get_param('product_multi_barcode_search.uniq_barcode')
            if limit_unique == 'True' or limit_unique is True:
                # Check in product.product barcodes
                dup_product = self.env['product.product'].sudo().search([
                    ('barcode', '=', rec.name),
                    ('company_id', '=', rec.company_id.id)
                ])
                # Check in product.barcode (other records)
                dup_extra = self.sudo().search([
                    ('name', '=', rec.name),
                    ('company_id', '=', rec.company_id.id),
                    ('id', '!=', rec.id)
                ])
                if dup_product or dup_extra:
                    raise ValidationError(_("The barcode '%s' is already assigned to another product!") % rec.name)
