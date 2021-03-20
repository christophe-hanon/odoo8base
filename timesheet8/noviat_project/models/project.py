# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#
#    Copyright (c) 2009-2016 Noviat nv/sa (www.noviat.com).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class project_project(models.Model):
    _inherit = 'project.project'

    notes = fields.Text(string="Notes")


class project_task(models.Model):
    _inherit = 'project.task'

    default_invoice_type = fields.Selection(
        selection='_get_invoice_type',
        string='Default Invoicing Agreement', default='tm')
    default_invoice_state = fields.Selection(
        selection='_get_invoice_state',
        string='Default Invoicing Status', default='open')
    closed = fields.Boolean(
        related='stage_id.closed', readonly=True, store=True,
        string='Closed')

    @api.model
    def _get_invoice_type(self):
        return [('none', 'No Invoice'),
                ('fp', 'Fixed Price'),
                ('tm', 'Time & Materials'),
                ('sd', 'Support Card')]

    @api.model
    def _get_invoice_state(self):
        return [('na', 'Not Applicable'),
                ('done', 'Invoiced'),
                ('open', 'To be invoiced')]


class project_work(models.Model):
    _inherit = 'project.task.work'
    _order = 'started_at desc, partner_id, task_id'

    started_at = fields.Datetime(
        string='Started At',
        required=True)
    travel = fields.Boolean(
        string='Travel Expenses')
    invoice_type = fields.Selection(
        selection='_get_invoice_type', required=True,
        string='Invoicing Agreement', default='tm')
    invoice_state = fields.Selection(
        selection='_get_invoice_state', required=True,
        string='Invoicing Status', default='open')
    rate_multiplier = fields.Selection(
        selection=[('1', '100 %'),
                   ('1.5', '150 %'),
                   ('2', '200 %')],
        string='Billing Rate %',
        default='1', required=True)
    notes = fields.Text('Notes')
    partner_id = fields.Many2one(
        related='task_id.partner_id.commercial_partner_id',
        string='Partner', readonly=True, store=True)

    @api.model
    def _get_invoice_type(self):
        return self.env['project.task']._get_invoice_type()

    @api.model
    def _get_invoice_state(self):
        return self.env['project.task']._get_invoice_state()

    @api.onchange('task_id')
    def _onchange_task_id(self):
        if self.task_id:
            self.invoice_type = self.task_id.default_invoice_type
            self.invoice_state = self.task_id.default_invoice_state

    def _create_analytic_entries(self, cr, uid, vals, context=None):
        if not context:
            context = {}
        context.update({
            'started_at': vals.get('started_at'),
            'travel': vals.get('travel'),
            'rate_multiplier': vals.get('rate_multiplier')
            })
        return super(project_work, self)._create_analytic_entries(
            cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        res = super(project_work, self).write(
            cr, uid, ids, vals, context=context)
        ts_obj = self.pool['hr.analytic.timesheet']
        for task in self.browse(cr, uid, ids, context=context):
            line_id = task.hr_analytic_timesheet_id
            if not line_id:
                continue
            vals_line = {}
            if 'started_at' in vals:
                vals_line['started_at'] = vals['started_at']
            if 'travel' in vals:
                vals_line['travel'] = vals['travel']
            if 'rate_multiplier' in vals:
                vals_line['rate_multiplier'] = vals['rate_multiplier']
            ts_obj.write(cr, uid, [line_id.id], vals_line, context=context)
        return res
