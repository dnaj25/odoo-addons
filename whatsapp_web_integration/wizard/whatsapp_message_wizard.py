# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import urllib.parse

class WhatsappMessageWizard(models.TransientModel):
    _name = 'whatsapp.message.wizard'
    _description = 'WhatsApp Message Wizard'

    partner_id = fields.Many2one('res.partner', string='Recipient', required=True)
    phone = fields.Char(string='WhatsApp Number', required=True, help="Enter phone number in international format without symbols (e.g. 966500000000)")
    message = fields.Text(string='Message', required=True)

    @api.model
    def default_get(self, fields_list):
        res = super(WhatsappMessageWizard, self).default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        
        if not active_model or not active_id:
            return res
            
        record = self.env[active_model].browse(active_id)
        partner = False
        message = ""
        
        if active_model == 'res.partner':
            partner = record
            message = _("Hello %s,\n") % partner.name
        elif active_model == 'sale.order':
            partner = record.partner_id
            message = _("Hello %s,\n\nHere is your Sale Order *%s* details:\nAmount: %s %s\nLink: %s/mail/view?model=sale.order&res_id=%s\n\nThank you!") % (
                partner.name,
                record.name,
                record.amount_total,
                record.currency_id.symbol,
                record.get_base_url(),
                record.id
            )
        elif active_model == 'account.move':
            partner = record.partner_id
            message = _("Hello %s,\n\nHere is your Invoice *%s* details:\nAmount: %s %s\nDue Date: %s\nLink: %s/mail/view?model=account.move&res_id=%s\n\nThank you!") % (
                partner.name,
                record.name,
                record.amount_total,
                record.currency_id.symbol,
                record.invoice_date_due,
                record.get_base_url(),
                record.id
            )
        elif active_model == 'purchase.order':
            partner = record.partner_id
            message = _("Hello %s,\n\nHere is our Purchase Order *%s* details:\nAmount: %s %s\nLink: %s/mail/view?model=purchase.order&res_id=%s\n\nPlease confirm.") % (
                partner.name,
                record.name,
                record.amount_total,
                record.currency_id.symbol,
                record.get_base_url(),
                record.id
            )

        if partner:
            res['partner_id'] = partner.id
            raw_phone = getattr(partner, 'mobile', '') or partner.phone or ""
            # Simple sanitization
            clean_phone = ''.join(c for c in raw_phone if c.isdigit())
            if clean_phone.startswith('00'):
                clean_phone = clean_phone[2:]
            res['phone'] = clean_phone
            res['message'] = message
            
        return res

    def action_send_whatsapp(self):
        self.ensure_one()
        if not self.phone:
            raise UserError(_("Please specify a valid WhatsApp number."))
            
        # Clean phone number
        clean_phone = ''.join(c for c in self.phone if c.isdigit())
        if clean_phone.startswith('00'):
            clean_phone = clean_phone[2:]
            
        # URL encode message
        encoded_message = urllib.parse.quote(self.message)
        
        # WhatsApp URL redirect link (supports both web and app)
        whatsapp_url = "https://web.whatsapp.com/send?phone=%s&text=%s" % (clean_phone, encoded_message)
        
        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_url,
            'target': 'new',
        }
