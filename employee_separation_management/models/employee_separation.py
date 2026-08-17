from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    basic_salary = fields.Float(string='Basic Salary', default=0.0, groups="hr.group_hr_user")
    joining_date = fields.Date(string='Joining Date', default=fields.Date.context_today, groups="hr.group_hr_user")

class HrEmployeeSeparation(models.Model):
    _name = 'hr.employee.separation'
    _description = 'Employee Exit & Final Settlement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'request_date desc, id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        required=True,
        tracking=True,
        readonly=True,
        states={'draft': [('readonly', '=', False)]}
    )
    department_id = fields.Many2one(
        'hr.department',
        related='employee_id.department_id',
        string='Department',
        readonly=True
    )
    job_id = fields.Many2one(
        'hr.job',
        related='employee_id.job_id',
        string='Job Position',
        readonly=True
    )
    request_date = fields.Date(
        string='Request Date',
        default=fields.Date.context_today,
        required=True,
        readonly=True,
        states={'draft': [('readonly', '=', False)]}
    )
    last_day_date = fields.Date(
        string='Last Day of Work',
        required=True,
        readonly=True,
        states={'draft': [('readonly', '=', False)]}
    )
    departure_reason = fields.Selection([
        ('resigned', 'Resignation'),
        ('fired', 'Termination/Dismissal'),
        ('retired', 'Retirement'),
        ('end_contract', 'End of Contract'),
    ], string='Departure Reason', required=True, default='resigned', readonly=True, states={'draft': [('readonly', '=', False)]})

    joining_date = fields.Date(
        string='Joining Date',
        related='employee_id.joining_date',
        readonly=False,
        store=True
    )
    wage = fields.Float(
        string='Basic Salary',
        related='employee_id.basic_salary',
        readonly=False,
        store=True
    )
    
    # Settlement Earnings
    gratuity_amount = fields.Float(
        string='Gratuity (End of Service)',
        readonly=True,
        digits=(16, 2)
    )
    remaining_leaves = fields.Float(
        string='Remaining Leave Balance (Days)',
        compute='_compute_leaves',
        store=True,
        readonly=True
    )
    leave_encashment_amount = fields.Float(
        string='Leave Encashment',
        readonly=True,
        digits=(16, 2)
    )
    overtime_amount = fields.Float(
        string='Overtime Amount',
        default=0.0,
        readonly=True,
        states={'draft': [('readonly', '=', False)], 'submit': [('readonly', '=', False)]},
        digits=(16, 2)
    )
    other_allowances = fields.Float(
        string='Other Allowances',
        default=0.0,
        readonly=True,
        states={'draft': [('readonly', '=', False)], 'submit': [('readonly', '=', False)]},
        digits=(16, 2)
    )

    # Settlement Deductions
    loan_deduction = fields.Float(
        string='Loan / Advance Deduction',
        default=0.0,
        readonly=True,
        states={'draft': [('readonly', '=', False)], 'submit': [('readonly', '=', False)]},
        digits=(16, 2)
    )
    other_deductions = fields.Float(
        string='Other Deductions / Asset Damage',
        default=0.0,
        readonly=True,
        states={'draft': [('readonly', '=', False)], 'submit': [('readonly', '=', False)]},
        digits=(16, 2)
    )

    # Total Net
    total_settlement = fields.Float(
        string='Net Settlement Amount',
        compute='_compute_total_settlement',
        store=True,
        digits=(16, 2)
    )
    
    notes = fields.Text(string='Notes/Remarks')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('hr_approve', 'HR Approved'),
        ('finance_approve', 'Finance Approved'),
        ('done', 'Settled'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, default='draft', tracking=True)

    @api.depends('employee_id')
    def _compute_leaves(self):
        for rec in self:
            if rec.employee_id:
                rec.remaining_leaves = rec.employee_id.remaining_leaves
            else:
                rec.remaining_leaves = 0.0

    @api.depends('gratuity_amount', 'leave_encashment_amount', 'overtime_amount', 'other_allowances', 'loan_deduction', 'other_deductions')
    def _compute_total_settlement(self):
        for rec in self:
            rec.total_settlement = (
                rec.gratuity_amount +
                rec.leave_encashment_amount +
                rec.overtime_amount +
                rec.other_allowances -
                rec.loan_deduction -
                rec.other_deductions
            )

    def action_compute_sheet(self):
        for rec in self:
            if not rec.employee_id:
                raise UserError(_("Please select an employee first."))
            if not rec.joining_date:
                raise UserError(_("Please specify the employee's joining date."))
            if not rec.last_day_date:
                raise UserError(_("Please specify the last day of work."))
            if rec.last_day_date < rec.joining_date:
                raise UserError(_("Last day of work cannot be before the joining date."))

            # 1. Gratuity Calculation (End of Service Benefits)
            service_days = (rec.last_day_date - rec.joining_date).days
            service_years = service_days / 365.25
            
            gratuity = 0.0
            if service_years >= 1.0:
                if service_years <= 5.0:
                    gratuity = service_years * (rec.wage * 15.0 / 30.0)
                else:
                    first_five = 5.0 * (rec.wage * 15.0 / 30.0)
                    remaining_years = service_years - 5.0
                    gratuity = first_five + (remaining_years * rec.wage)
            rec.gratuity_amount = gratuity

            # 2. Leave Encashment Calculation
            daily_salary = rec.wage / 30.0
            rec.leave_encashment_amount = max(0.0, rec.remaining_leaves * daily_salary)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.employee.separation') or _('New')
        return super(HrEmployeeSeparation, self).create(vals)

    def action_submit(self):
        self.action_compute_sheet()
        self.write({'state': 'submit'})

    def action_hr_approve(self):
        self.write({'state': 'hr_approve'})

    def action_finance_approve(self):
        self.write({'state': 'finance_approve'})

    def action_done(self):
        self.write({'state': 'done'})
        if self.employee_id:
            self.employee_id.write({
                'active': False,
                'departure_reason_id': self.env['hr.departure.reason'].search([('name', '=', self.departure_reason)], limit=1).id or False,
                'departure_date': self.last_day_date
            })

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_draft(self):
        self.write({'state': 'draft'})
