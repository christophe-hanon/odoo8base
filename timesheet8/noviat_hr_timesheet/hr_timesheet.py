# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#
#    Copyright (c) 2010-2015 Noviat nv/sa (www.noviat.com).
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

from openerp import models, fields


class hr_analytic_timesheet(models.Model):
    _inherit = 'hr.analytic.timesheet'

    started_at = fields.Datetime(string='Started At', required=True)
    travel = fields.Boolean(string='Travel Expenses')
    rate_multiplier = fields.Selection([
        ('1', '100 %'),
        ('1.5', '150 %'),
        ('2', '200 %'),
        ], string='Billing Rate %', required=True)

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if 'started_at' not in vals:
            vals['started_at'] = context.get('started_at') \
                or fields.Datetime.now()
        if 'travel' not in vals:
            vals['travel'] = context.get('travel', False)
        if 'rate_multiplier' not in vals:
            vals['rate_multiplier'] = context.get('rate_multiplier') or '1'
        return super(hr_analytic_timesheet, self).create(
            cr, uid, vals, context=context)
