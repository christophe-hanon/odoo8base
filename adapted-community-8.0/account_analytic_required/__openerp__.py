# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account analytic required module for OpenERP
#    Copyright (C) 2011 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Account Analytic Required',
    'version': '8.0.0.3.0',
    'category': 'Analytic Accounting',
    'license': 'AGPL-3',
    'summary': 'Account Analytic Required',
    'author': "Akretion,"
              "Odoo Community Association (OCA)",
    'depends': ['account'],
    'data': [
        'views/account_account_type.xml',
        'views/account_invoice.xml',
        'views/account_move.xml',
        'views/account_template.xml',
        ],
    'installable': True,
}
