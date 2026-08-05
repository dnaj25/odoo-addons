from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    barcode_ids = fields.One2many('product.barcode', 'product_tmpl_id', string='Extra Barcodes')

class ProductProduct(models.Model):
    _inherit = 'product.product'

    barcode_ids = fields.One2many('product.barcode', 'product_id', string='Extra Barcodes')

    @api.model
    def _search_display_name(self, operator, value):
        domain = super()._search_display_name(operator, value)
        if operator in ('=', 'ilike', 'like', 'in'):
            # Find products matching the extra barcodes
            extra_domain = [('barcode_ids.name', operator, value)]
            extra_products = self.sudo().search(extra_domain)
            if extra_products:
                from odoo.osv import expression
                domain = expression.OR([domain, [('id', 'in', extra_products.ids)]])
        return domain

    @api.model
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            if operator in positive_operators:
                products = self.search([('barcode_ids.name', '=', name)] + (domain or []), limit=limit)
                if products:
                    return [(p.id, p.display_name) for p in products]
        return super().name_search(name, domain, operator, limit)
