# -*- coding: utf-8 -*-
import base64
from odoo import http
from odoo.http import request

class MobileApiController(http.Controller):

    def _get_base_url(self):
        return request.env['ir.config_parameter'].sudo().get_param('web.base.url')

    @http.route('/mobile/api/v1/homepage', type='json', auth='public', methods=['POST', 'GET'], csrf=False)
    def get_homepage_data(self):
        # 1. Fetch Banners
        banners = request.env['mobile.banner'].sudo().search([('active', '=', True)])
        banner_list = []
        base_url = self._get_base_url()
        for banner in banners:
            action_val = ""
            if banner.action_type == 'category' and banner.category_id:
                action_val = str(banner.category_id.id)
            elif banner.action_type == 'product' and banner.product_id:
                action_val = str(banner.product_id.id)
            elif banner.action_type == 'url':
                action_val = banner.custom_url

            banner_list.append({
                'id': banner.id,
                'name': banner.name,
                'action_type': banner.action_type,
                'action_value': action_val,
                'image_url': f"{base_url}/web/image/mobile.banner/{banner.id}/image"
            })

        # 2. Fetch Featured Products (Website Published Products)
        products = request.env['product.template'].sudo().search([
            ('sale_ok', '=', True),
            ('is_published', '=', True)
        ], limit=8)
        
        product_list = []
        for prod in products:
            product_list.append({
                'id': prod.id,
                'name': prod.name,
                'price': prod.list_price,
                'image_url': f"{base_url}/web/image/product.template/{prod.id}/image_1920"
            })

        return {
            'status': 'success',
            'banners': banner_list,
            'featured_products': product_list
        }

    @http.route('/mobile/api/v1/products', type='json', auth='public', methods=['POST'], csrf=False)
    def get_products(self, category_id=None, search=None, limit=20, offset=0):
        domain = [('sale_ok', '=', True), ('is_published', '=', True)]
        if category_id:
            domain.append(('public_categ_ids', 'in', [int(category_id)]))
        if search:
            domain.append(('name', 'ilike', search))

        products = request.env['product.template'].sudo().search(domain, limit=limit, offset=offset)
        base_url = self._get_base_url()
        product_list = []
        for prod in products:
            product_list.append({
                'id': prod.id,
                'name': prod.name,
                'price': prod.list_price,
                'image_url': f"{base_url}/web/image/product.template/{prod.id}/image_1920",
                'description': prod.description_sale or ""
            })

        return {
            'status': 'success',
            'products': product_list
        }

    @http.route('/mobile/api/v1/auth/login', type='json', auth='none', methods=['POST'], csrf=False)
    def login_user(self, login, password):
        try:
            uid = request.session.authenticate(request.db, login, password)
            if uid:
                user = request.env['res.users'].sudo().browse(uid)
                partner = user.partner_id
                return {
                    'status': 'success',
                    'session_id': request.session.sid,
                    'uid': uid,
                    'user': {
                        'name': partner.name,
                        'email': partner.email,
                        'phone': partner.phone or ""
                    }
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
        return {
            'status': 'error',
            'message': 'Invalid login credentials'
        }

    @http.route('/mobile/api/v1/cart', type='json', auth='public', methods=['POST'], csrf=False)
    def get_or_update_cart(self, product_id=None, add_qty=None, set_qty=None):
        # Odoo's website_sale cart flow
        sale_order = request.website.sale_get_order(force_create=True)
        if product_id:
            sale_order._cart_update(
                product_id=int(product_id),
                add_qty=float(add_qty) if add_qty else None,
                set_qty=float(set_qty) if set_qty else None
            )

        base_url = self._get_base_url()
        lines = []
        for line in sale_order.order_line:
            lines.append({
                'id': line.id,
                'product_id': line.product_id.id,
                'name': line.name,
                'quantity': line.product_uom_qty,
                'price_unit': line.price_unit,
                'price_subtotal': line.price_subtotal,
                'image_url': f"{base_url}/web/image/product.product/{line.product_id.id}/image_1920"
            })

        return {
            'status': 'success',
            'cart': {
                'order_id': sale_order.id,
                'name': sale_order.name,
                'amount_total': sale_order.amount_total,
                'amount_untaxed': sale_order.amount_untaxed,
                'amount_tax': sale_order.amount_tax,
                'lines': lines
            }
        }
