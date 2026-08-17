# -*- coding: utf-8 -*-
from odoo import models, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_open_label_layout(self):
        # Collect all unique storable/consumable products from order lines
        products = self.order_line.filtered(
            lambda l: l.product_id and not l.display_type and l.product_id.type in ('consu', 'product')
        ).mapped('product_id')
        
        view = self.env.ref('sale_product_label.product_label_layout_form_sale')
        return {
            'name': _('Choose Labels Layout'),
            'type': 'ir.actions.act_window',
            'res_model': 'product.label.layout',
            'views': [(view.id, 'form')],
            'target': 'new',
            'context': {
                'default_product_ids': products.ids,
                'default_sale_order_ids': self.ids,
                'default_sale_quantity': 'sale',
            },
        }
