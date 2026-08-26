from odoo import models, fields, api, _
from datetime import date, timedelta
from odoo.exceptions import UserError

class ContractContract(models.Model):
    _name = 'contract.contract'
    _description = 'Contract Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'end_date asc, id desc'

    name = fields.Char(string='Contract Title / Ref', required=True, tracking=True)
    contract_type_id = fields.Many2one('contract.type', string='Contract Type', required=True, tracking=True)
    
    # أطراف العقد والمسؤول
    partner_id = fields.Many2one('res.partner', string='Partner / Vendor / Customer', tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee (If HR Contract)', tracking=True)
    responsible_id = fields.Many2one('res.users', string='Contract Manager', default=lambda self: self.env.user, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    # التواريخ والتنبيهات
    start_date = fields.Date(string='Start Date', required=True, tracking=True)
    end_date = fields.Date(string='End Date', required=True, tracking=True)
    days_to_expire = fields.Integer(string='Days Until Expiry', compute='_compute_days_to_expire', store=True)
    alert_days = fields.Selection([
        ('2', '2 Days'),
        ('7', '7 Days'),
        ('15', '15 Days'),
        ('30', '30 Days'),
        ('60', '60 Days'),
        ('90', '90 Days'),
    ], string='Alert Trigger Window', default='2', required=True)

    # التفاصيل المالية والمرفقات
    amount = fields.Monetary(string='Contract Value', currency_field='currency_id', tracking=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    notes = fields.Html(string='Terms & Description')
    
    # حالات العقد
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expiring', 'Expiring Soon'),
        ('expired', 'Expired'),
        ('renewed', 'Renewed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, index=True)

    # سجل التجديدات والمرفقات
    renewal_log_ids = fields.One2many('contract.renewal.log', 'contract_id', string='Renewal History')
    renewal_count = fields.Integer(compute='_compute_renewal_count', string='Renewals Count')

    @api.depends('end_date')
    def _compute_days_to_expire(self):
        today = fields.Date.today()
        for rec in self:
            if rec.end_date:
                rec.days_to_expire = (rec.end_date - today).days
            else:
                rec.days_to_expire = 0

    @api.depends('renewal_log_ids')
    def _compute_renewal_count(self):
        for rec in self:
            rec.renewal_count = len(rec.renewal_log_ids)

    def action_activate(self):
        self.write({'state': 'active'})

    def action_renew(self):
        """فتح نافذة تجديد العقد وحفظ السجل القديم"""
        self.ensure_one()
        return {
            'name': _('Renew Contract'),
            'type': 'ir.actions.act_window',
            'res_model': 'contract.renewal.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_contract_id': self.id,
                'default_old_start_date': self.start_date,
                'default_old_end_date': self.end_date,
                'default_old_amount': self.amount,
                'default_new_start_date': self.end_date or fields.Date.today(),
                'default_new_amount': self.amount,
            }
        }

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    @api.model
    def _cron_check_contract_expiry(self):
        """مهمة تلقائية تعمل يومياً لفحص العقود القريبة من الانتهاء"""
        today = fields.Date.today()
        contracts = self.search([('state', 'in', ['active', 'expiring'])])
        
        for contract in contracts:
            if not contract.end_date:
                continue
            
            days_left = (contract.end_date - today).days
            alert_limit = int(contract.alert_days)

            # حالة منتهي
            if days_left <= 0:
                contract.write({'state': 'expired'})
                contract._create_expiry_activity(_("Contract %s has expired!") % contract.name)
                contract._send_discuss_notification(_("⚠️ Expiry Alert: Contract '%s' has expired on %s!") % (contract.name, contract.end_date))
            
            # حالة وشيك الانتهاء (أقل من أو تساوي الأيام المحددة للتنبيه)
            elif days_left <= alert_limit:
                contract.write({'state': 'expiring'})
                contract._create_expiry_activity(_("Contract %s will expire in %d days.") % (contract.name, days_left))
                contract._send_discuss_notification(_("⏰ Expiry Warning: Contract '%s' will expire in %d days (on %s).") % (contract.name, days_left, contract.end_date))

    def _create_expiry_activity(self, note):
        """إنشاء نشاط/تنبيه للمسؤول عن العقد"""
        model_id = self.env['ir.model']._get_id('contract.contract')
        for rec in self:
            existing_activity = self.env['mail.activity'].search([
                ('res_model', '=', 'contract.contract'),
                ('res_id', '=', rec.id),
                ('activity_type_id', '=', self.env.ref('mail.mail_activity_data_todo').id),
                ('user_id', '=', rec.responsible_id.id)
            ], limit=1)
            
            if not existing_activity:
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'note': note,
                    'summary': _('Contract Expiry Notice'),
                    'user_id': rec.responsible_id.id,
                    'res_id': rec.id,
                    'res_model': 'contract.contract',
                    'res_model_id': model_id,
                    'date_deadline': rec.end_date,
                })

    def _send_discuss_notification(self, body):
        """إرسال إشعار من OdooBot يظهر فوراً في شاشة Notifications"""
        odoobot_partner = self.env.ref('base.partner_root', raise_if_not_found=False)
        for rec in self:
            if rec.responsible_id and rec.responsible_id.partner_id:
                rec.message_post(
                    body=body,
                    message_type='comment',
                    subtype_xmlid='mail.mt_comment',
                    author_id=odoobot_partner.id if odoobot_partner else False,
                    partner_ids=[rec.responsible_id.partner_id.id],
                )