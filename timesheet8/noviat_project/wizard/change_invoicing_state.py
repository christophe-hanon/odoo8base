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

from openerp.osv import orm, fields


class task_work_change_invoicing_state(orm.TransientModel):
    _name = 'task.work.change.invoicing.state'
    _description = 'Change Invoicing State of selected items'

    _columns = {
        'invoice_state': fields.selection([
            ('na', 'Not Applicable'),
            ('done', 'Invoiced'),
            ('open', 'To be invoiced'),
        ], 'Invoicing Status', required=True),
    }

    def change_state(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        line_ids = context.get('active_ids')
        work_obj = self.pool['project.task.work']
        for wiz in self.browse(cr, uid, ids, context=context):
            work_obj.write(
                cr, uid, line_ids,
                {'invoice_state': wiz.invoice_state}, context=context)
        return {'type': 'ir.actions.act_window_close'}
