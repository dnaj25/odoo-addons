# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from datetime import date, datetime

class PrepaidExpense(models.Model):
    _name = 'prepaid.expense'
    _description = 'Prepaid Expense Contract / Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc, id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True
    )
    title = fields.Char(
        string='Contract / Expense Title',
        required=True,
        tracking=True,
        placeholder='e.g., Head Office Rent 2026, Cloud Server Subscription'
    )
    category_id = fields.Many2one(
        'prepaid.expense.type',
        string='Expense Category',
        required=True,
        tracking=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Vendor / Landlord / Payee',
        tracking=True
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='company_id.currency_id',
        readonly=True
    )
    user_id = fields.Many2one(
        'res.users',
        string='Responsible Person',
        default=lambda self: self.env.user,
        tracking=True
    )
    
    # Financial Accounts
    total_amount = fields.Monetary(
        string='Total Prepaid Amount',
        required=True,
        currency_field='currency_id',
        tracking=True
    )
    prepaid_account_id = fields.Many2one(
        'account.account',
        string='Prepaid Asset Account',
        required=True,
        domain="[('deprecated', '=', False)]",
        help='Account holding the prepaid balance (Debit on initial bill, Credit on periodic recognition)'
    )
    expense_account_id = fields.Many2one(
        'account.account',
        string='Expense Account (P&L)',
        required=True,
        domain="[('deprecated', '=', False)]",
        help='P&L account recognized each period (Debit Expense)'
    )
    journal_id = fields.Many2one(
        'account.journal',
        string='Recognition Journal',
        required=True,
        domain="[('type', 'in', ['general', 'purchase'])]",
        default=lambda self: self.env['account.journal'].search([('type', '=', 'general')], limit=1)
    )
    source_invoice_id = fields.Many2one(
        'account.move',
        string='Source Vendor Bill',
        domain="[('move_type', 'in', ['in_invoice', 'in_receipt'])]",
        help='Optional link to the original bill where prepaid payment was recorded'
    )
    analytic_distribution = fields.Json(
        string='Analytic Distribution',
        help='Cost centers / Analytic accounts distribution for recognized expenses'
    )

    # Timing & Periodicity
    start_date = fields.Date(
        string='Start Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True
    )
    end_date = fields.Date(
        string='End Date',
        required=True,
        tracking=True
    )
    periodicity = fields.Selection([
        ('monthly', 'Monthly (Every Month)'),
        ('quarterly', 'Quarterly (Every 3 Months)'),
        ('semi_annually', 'Semi-Annually (Every 6 Months)'),
        ('annually', 'Annually (Once a Year)'),
        ('custom', 'Custom Number of Periods'),
    ], string='Recognition Frequency', default='monthly', required=True, tracking=True)
    
    number_of_periods = fields.Integer(
        string='Number of Periods',
        compute='_compute_number_of_periods',
        store=True,
        readonly=False,
        help='Calculated number of deduction installments'
    )
    auto_post = fields.Boolean(
        string='Auto-Post via Cron',
        default=True,
        help='If checked, the system automated cron job will automatically post entries when the due date arrives'
    )

    # Expiration & Renewal Reminder
    reminder_days_before = fields.Integer(
        string='Renewal Notice (Days)',
        default=30,
        help='Number of days before the contract ends to trigger the last-month renewal alert'
    )
    days_to_expire = fields.Integer(
        string='Days to Expiration',
        compute='_compute_renewal_status',
        store=True
    )
    is_expiring_soon = fields.Boolean(
        string='Expiring Soon (Last Month)',
        compute='_compute_renewal_status',
        store=True
    )
    renewal_state = fields.Selection([
        ('normal', 'Active & In Good Standing'),
        ('expiring_soon', '⚠️ Expiring Soon (Final Month / Action Required)'),
        ('expired', 'Expired'),
        ('renewed', 'Renewed'),
    ], string='Renewal Status', compute='_compute_renewal_status', store=True, tracking=True)

    # Lines & Metrics
    line_ids = fields.One2many(
        'prepaid.expense.line',
        'expense_id',
        string='Schedule Lines',
        copy=False
    )
    lines_count = fields.Integer(
        string='Total Installments',
        compute='_compute_metrics',
        store=True
    )
    posted_lines_count = fields.Integer(
        string='Recognized Installments',
        compute='_compute_metrics',
        store=True
    )
    posted_amount = fields.Monetary(
        string='Total Recognized Amount',
        compute='_compute_metrics',
        store=True,
        currency_field='currency_id'
    )
    remaining_amount = fields.Monetary(
        string='Remaining Prepaid Balance',
        compute='_compute_metrics',
        store=True,
        currency_field='currency_id'
    )
    move_count = fields.Integer(
        string='Journal Entries Count',
        compute='_compute_move_count'
    )

    # State Workflow
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed & Active'),
        ('done', 'Fully Recognized & Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True)

    notes = fields.Html(string='Internal Notes & Terms')

    # ==========================
    # COMPUTE METHODS
    # ==========================
    @api.onchange('category_id')
    def _onchange_category_id(self):
        if self.category_id:
            if self.category_id.prepaid_account_id:
                self.prepaid_account_id = self.category_id.prepaid_account_id
            if self.category_id.expense_account_id:
                self.expense_account_id = self.category_id.expense_account_id
            if self.category_id.journal_id:
                self.journal_id = self.category_id.journal_id
            if self.category_id.default_periodicity:
                self.periodicity = self.category_id.default_periodicity
            if self.category_id.reminder_days_before:
                self.reminder_days_before = self.category_id.reminder_days_before

    @api.depends('start_date', 'end_date', 'periodicity')
    def _compute_number_of_periods(self):
        for rec in self:
            if not rec.start_date or not rec.end_date or rec.start_date > rec.end_date:
                rec.number_of_periods = 1
                continue
            
            if rec.periodicity == 'custom':
                if not rec.number_of_periods or rec.number_of_periods <= 0:
                    rec.number_of_periods = 12
                continue
            
            diff = relativedelta(rec.end_date, rec.start_date)
            total_months = diff.years * 12 + diff.months
            if diff.days > 0:
                total_months += 1
            
            if total_months <= 0:
                total_months = 1
                
            if rec.periodicity == 'monthly':
                rec.number_of_periods = total_months
            elif rec.periodicity == 'quarterly':
                rec.number_of_periods = max(1, round(total_months / 3))
            elif rec.periodicity == 'semi_annually':
                rec.number_of_periods = max(1, round(total_months / 6))
            elif rec.periodicity == 'annually':
                rec.number_of_periods = max(1, round(total_months / 12))
            else:
                rec.number_of_periods = max(1, total_months)

    @api.depends('end_date', 'reminder_days_before', 'state')
    def _compute_renewal_status(self):
        today = fields.Date.context_today(self)
        for rec in self:
            if not rec.end_date or rec.state in ['draft', 'cancelled']:
                rec.days_to_expire = 0
                rec.is_expiring_soon = False
                rec.renewal_state = 'normal'
                continue

            delta = (rec.end_date - today).days
            rec.days_to_expire = delta
            notice_limit = rec.reminder_days_before if rec.reminder_days_before > 0 else 30

            if delta < 0:
                rec.is_expiring_soon = False
                rec.renewal_state = 'expired'
            elif delta <= notice_limit:
                rec.is_expiring_soon = True
                rec.renewal_state = 'expiring_soon'
            else:
                rec.is_expiring_soon = False
                rec.renewal_state = 'normal'

    @api.depends('line_ids', 'line_ids.state', 'line_ids.amount', 'total_amount')
    def _compute_metrics(self):
        for rec in self:
            lines = rec.line_ids
            posted_lines = lines.filtered(lambda l: l.state == 'posted')
            rec.lines_count = len(lines)
            rec.posted_lines_count = len(posted_lines)
            rec.posted_amount = sum(posted_lines.mapped('amount'))
            rec.remaining_amount = rec.total_amount - rec.posted_amount
            
            if rec.state == 'confirmed' and rec.lines_count > 0 and len(posted_lines) == rec.lines_count:
                rec.state = 'done'

    def _compute_move_count(self):
        for rec in self:
            rec.move_count = self.env['account.move'].search_count([
                ('id', 'in', rec.line_ids.mapped('move_id').ids)
            ])

    # ==========================
    # BUSINESS ACTIONS
    # ==========================
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('prepaid.expense') or _('New')
        return super(PrepaidExpense, self).create(vals_list)

    def action_compute_schedule(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('You can only compute or reset the schedule while in Draft status.'))
        if self.total_amount <= 0:
            raise ValidationError(_('Total prepaid amount must be greater than zero.'))
        if not self.start_date or not self.end_date or self.start_date >= self.end_date:
            raise ValidationError(_('Start Date must be strictly before End Date.'))
        if self.number_of_periods <= 0:
            raise ValidationError(_('Number of periods must be at least 1.'))

        self.line_ids.unlink()

        periods = self.number_of_periods
        base_amount = round(self.total_amount / periods, 2)
        accumulated = 0.0
        
        if self.periodicity == 'monthly':
            interval = relativedelta(months=1)
        elif self.periodicity == 'quarterly':
            interval = relativedelta(months=3)
        elif self.periodicity == 'semi_annually':
            interval = relativedelta(months=6)
        elif self.periodicity == 'annually':
            interval = relativedelta(years=1)
        else:
            total_days = (self.end_date - self.start_date).days
            days_step = max(1, round(total_days / periods))
            interval = relativedelta(days=days_step)

        line_vals = []
        current_date = self.start_date
        
        for i in range(1, periods + 1):
            if i == periods:
                amount = round(self.total_amount - accumulated, 2)
                line_date = self.end_date
            else:
                amount = base_amount
                accumulated += amount
                line_date = current_date
                current_date = current_date + interval
                if line_date > self.end_date:
                    line_date = self.end_date

            line_vals.append({
                'expense_id': self.id,
                'sequence': i,
                'name': f"{self.name} - Period {i}/{periods}",
                'date': line_date,
                'amount': amount,
                'state': 'draft',
            })

        self.env['prepaid.expense.line'].create(line_vals)
        return True

    def action_confirm(self):
        self.ensure_one()
        if not self.line_ids:
            self.action_compute_schedule()
        if not self.line_ids:
            raise UserError(_('Cannot confirm a prepaid expense with no schedule lines.'))
        self.state = 'confirmed'
        self.message_post(body=_('Prepaid expense contract confirmed with %s scheduled installments.') % len(self.line_ids))

    def action_post_due_entries(self):
        self.ensure_one()
        today = fields.Date.context_today(self)
        due_lines = self.line_ids.filtered(lambda l: l.state == 'draft' and l.date <= today)
        if not due_lines:
            raise UserError(_('No due installments found on or before today (%s).') % today)
        for line in due_lines:
            line.action_post_entry()
        self.message_post(body=_('%s due recognition entries have been posted successfully.') % len(due_lines))

    def action_cancel(self):
        self.ensure_one()
        posted_lines = self.line_ids.filtered(lambda l: l.state == 'posted')
        if posted_lines:
            raise UserError(_('Cannot cancel this contract because some entries are already posted. Please reverse the journal entries first.'))
        self.state = 'cancelled'
        self.line_ids.write({'state': 'cancelled'})

    def action_reset_to_draft(self):
        self.ensure_one()
        posted_lines = self.line_ids.filtered(lambda l: l.state == 'posted')
        if posted_lines:
            raise UserError(_('Cannot reset to draft while posted entries exist.'))
        self.state = 'draft'
        self.line_ids.write({'state': 'draft'})

    def action_renew(self):
        self.ensure_one()
        new_start = self.end_date + relativedelta(days=1)
        diff = relativedelta(self.end_date, self.start_date)
        new_end = new_start + diff

        new_vals = {
            'title': _('%s (Renewed)') % self.title,
            'category_id': self.category_id.id,
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'user_id': self.user_id.id,
            'total_amount': self.total_amount,
            'prepaid_account_id': self.prepaid_account_id.id,
            'expense_account_id': self.expense_account_id.id,
            'journal_id': self.journal_id.id,
            'start_date': new_start,
            'end_date': new_end,
            'periodicity': self.periodicity,
            'number_of_periods': self.number_of_periods,
            'reminder_days_before': self.reminder_days_before,
            'analytic_distribution': self.analytic_distribution,
            'state': 'draft',
        }
        new_rec = self.create(new_vals)
        new_rec.action_compute_schedule()
        
        self.renewal_state = 'renewed'
        self.message_post(body=_('Contract renewed! New contract reference: %s') % new_rec.name)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'prepaid.expense',
            'res_id': new_rec.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_journal_entries(self):
        self.ensure_one()
        move_ids = self.line_ids.mapped('move_id').ids
        return {
            'name': _('Recognition Journal Entries: %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', move_ids)],
        }

    # ==========================
    # CRON AUTOMATIONS
    # ==========================
    @api.model
    def cron_auto_post_prepaid_entries(self):
        today = fields.Date.context_today(self)
        active_contracts = self.search([
            ('state', '=', 'confirmed'),
            ('auto_post', '=', True)
        ])
        lines_to_post = self.env['prepaid.expense.line'].search([
            ('expense_id', 'in', active_contracts.ids),
            ('state', '=', 'draft'),
            ('date', '<=', today)
        ])
        for line in lines_to_post:
            try:
                line.action_post_entry()
            except Exception as e:
                line.expense_id.message_post(
                    body=_('Automatic recognition failed for installment %s on date %s. Error: %s') % (line.name, line.date, str(e))
                )

    @api.model
    def cron_check_prepaid_expirations(self):
        today = fields.Date.context_today(self)
        active_contracts = self.search([('state', '=', 'confirmed')])
        activity_type = self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)

        for rec in active_contracts:
            delta = (rec.end_date - today).days
            notice_days = rec.reminder_days_before if rec.reminder_days_before > 0 else 30

            if 0 <= delta <= notice_days and rec.renewal_state != 'renewed':
                rec.renewal_state = 'expiring_soon'
                
                existing_act = self.env['mail.activity'].search([
                    ('res_model', '=', 'prepaid.expense'),
                    ('res_id', '=', rec.id),
                    ('user_id', '=', rec.user_id.id),
                    ('summary', 'like', _('Contract Expiring Soon'))
                ], limit=1)

                if not existing_act:
                    rec.activity_schedule(
                        activity_type_id=activity_type.id if activity_type else 1,
                        summary=_('Contract Expiring Soon - Renewal Required (%s days left)') % delta,
                        note=_('Prepaid contract %s (%s) expires on %s. Please review and initiate renewal or termination.') % (rec.name, rec.title, rec.end_date),
                        user_id=rec.user_id.id,
                        date_deadline=rec.end_date,
                    )
                    rec.message_post(
                        body=_('⚠️ <b>Renewal Notice:</b> This contract enters its final period. %s days remaining until expiration on %s.') % (delta, rec.end_date)
                    )
            elif delta < 0:
                rec.renewal_state = 'expired'
