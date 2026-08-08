# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    applied_on = fields.Selection(
        selection_add=[('4_attribute', 'Product Attribute')],
        ondelete={'4_attribute': 'cascade'}
    )
    
    display_applied_on = fields.Selection(
        selection_add=[('4_attribute', 'Product Attribute')],
        ondelete={'4_attribute': 'cascade'}
    )
    
    product_template_attribute_value_id = fields.Many2one(
        'product.template.attribute.value',
        string="Product Attribute Value",
        check_company=True,
        domain="[('product_tmpl_id', '=', product_tmpl_id)]"
    )

    @api.onchange('display_applied_on')
    def _onchange_display_applied_on(self):
        super()._onchange_display_applied_on()
        if self.display_applied_on == '4_attribute':
            self.applied_on = '4_attribute'
            self.categ_id = False
            self.product_id = False
        else:
            self.product_template_attribute_value_id = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('display_applied_on') == '4_attribute' and 'applied_on' not in vals:
                vals['applied_on'] = '4_attribute'
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('display_applied_on') == '4_attribute' and 'applied_on' not in vals:
            vals['applied_on'] = '4_attribute'
        return super().write(vals)

    def _is_applicable_for(self, product, qty_in_product_uom):
        res = super()._is_applicable_for(product, qty_in_product_uom)
        if not res:
            return False
            
        if self.applied_on == '4_attribute':
            is_product_template = product._name == 'product.template'
            if is_product_template:
                # If evaluating the template itself, match the template id
                if product.id != self.product_tmpl_id.id:
                    return False
            else:
                # If evaluating a product variant, match the template and the specific attribute value
                if product.product_tmpl_id.id != self.product_tmpl_id.id:
                    return False
                if self.product_template_attribute_value_id and self.product_template_attribute_value_id.id not in product.product_template_attribute_value_ids.ids:
                    return False
        return res
