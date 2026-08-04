import json
import urllib.request
import urllib.error
import logging
from odoo import models, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class GeminiService(models.AbstractModel):
    _name = 'gemini.service'
    _description = 'Gemini AI Service'

    @api.model
    def _get_odoo_context(self):
        """
        Gathers context from Odoo database records to pass to Gemini AI.
        """
        try:
            # 1. Fetch Taxes
            taxes = self.env['account.tax'].sudo().search([])
            taxes_list = [f"- Tax: {t.name} (Type: {t.type_tax_use}, Amount: {t.amount}%)" for t in taxes]
            taxes_str = "\n".join(taxes_list)

            # 2. Fetch Products
            products = self.env['product.template'].sudo().search([], limit=50)
            products_list = [f"- Product: {p.name} (Sale Price: {p.list_price} SAR, Taxes: {', '.join(p.taxes_id.mapped('name'))})" for p in products]
            products_str = "\n".join(products_list)

            # 3. Fetch Suppliers
            suppliers = self.env['res.partner'].sudo().search([('supplier_rank', '>', 0)], limit=50)
            suppliers_list = [f"- Supplier: {s.name} (Default Purchase Tax: {s.x_default_purchase_tax_id.name or 'None'})" for s in suppliers]
            suppliers_str = "\n".join(suppliers_list)

            # 4. Fetch Recent Purchase Orders
            pos = self.env['purchase.order'].sudo().search([], limit=10, order='id desc')
            pos_list = [f"- Purchase Order: {po.name} (Supplier: {po.partner_id.name}, Total: {po.amount_total} SAR, Status: {po.state})" for po in pos]
            pos_str = "\n".join(pos_list)

            context = f"""
[Odoo Current Database Context]
Taxes:
{taxes_str or "No taxes configured"}

Products:
{products_str or "No products found"}

Suppliers (Vendors):
{suppliers_str or "No suppliers found"}

Recent Purchase Orders:
{pos_str or "No purchase orders found"}
"""
            return context
        except Exception as e:
            _logger.error("Failed to gather Odoo database context: %s", e)
            return ""

    @api.model
    def generate_content(self, prompt):
        """
        Sends a generation request to the Gemini API and returns the generated text.
        """
        params = self.env['ir.config_parameter'].sudo()
        api_key = params.get_param('odoo_gemini.api_key')
        model_name = params.get_param('odoo_gemini.model_name', 'gemini-flash-latest')

        if not api_key:
            raise UserError(_("Please configure the Google Gemini API Key in Odoo Settings under General Settings -> Gemini AI."))

        # Fetch Odoo DB context dynamically and inject it to system instruction
        db_context = self._get_odoo_context()
        system_instruction = (
            "You are Odoo AI Assistant. You have real-time access to the user's Odoo database context "
            "provided below. Use this context to answer questions about products, suppliers, taxes, "
            "and purchase orders accurately in the language of the query (Arabic or English).\n"
        )
        full_prompt = f"{system_instruction}\n{db_context}\n\nUser Prompt: {prompt}"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": full_prompt
                        }
                    ]
                }
            ]
        }
        
        try:
            req = urllib.request.Request(
                url, 
                data=json.dumps(payload).encode('utf-8'), 
                headers=headers,
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                
                candidates = res_data.get('candidates', [])
                if candidates:
                    parts = candidates[0].get('content', {}).get('parts', [])
                    if parts:
                        return parts[0].get('text', '')
                
                raise UserError(_("Gemini API returned an empty response. Response payload: %s") % json.dumps(res_data))
        except urllib.error.HTTPError as e:
            err_content = e.read().decode('utf-8')
            _logger.error("Gemini API HTTP Error: %s - %s", e.code, err_content)
            try:
                err_json = json.loads(err_content)
                err_msg = err_json.get('error', {}).get('message', '')
            except Exception:
                err_msg = err_content
            raise UserError(_("Gemini API Error: %s") % err_msg)
        except Exception as e:
            _logger.exception("Failed to connect to Gemini API")
            raise UserError(_("Connection to Gemini API failed: %s") % str(e))
