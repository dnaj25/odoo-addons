# -*- coding: utf-8 -*-
from odoo import models, fields

class MobileBanner(models.Model):
    _name = 'mobile.banner'
    _description = 'Mobile App Promotion Banner'
    _order = 'sequence, id'

    name = fields.Char(string='Title', required=True)
    image = fields.Binary(string='Banner Image', required=True, attachment=True)
    sequence = fields.Integer(string='Sequence', default=10)
    action_type = fields.Selection([
        ('category', 'Public Category'),
        ('product', 'Product Template'),
        ('url', 'Custom URL')
    ], string='Action Type', default='category', required=True)
    
    product_id = fields.Many2one('product.template', string='Product')
    category_id = fields.Many2one('product.public.category', string='Public Category')
    custom_url = fields.Char(string='Custom URL')
    active = fields.Boolean(string='Active', default=True)
