# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2012-2015 Noviat nv/sa (www.noviat.com).
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
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Intrastat reports for Belgium',
    'version': '0.1',
    'category': 'Localisation/Reporting',
    'author': "Noviat, Odoo Community Association (OCA)",
    'summary': 'Belgian Intrastat declaration',
    'depends': [
        'l10n_be_partner',
        'intrastat_product',
        'stock'
    ],
    'conflicts': [
        'report_intrastat',
        'l10n_be_intrastat'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/intrastat_unit.xml',
        'data/intrastat_region.xml',
        'data/intrastat_transaction.xml',
        'data/intrastat_transport_mode.xml',
        'intrastat_view.xml',
        'res_company_view.xml',
        'stock_view.xml',
        'account_invoice_view.xml',
        'l10n_be_intrastat_view.xml',
        'intrastat_installer_view.xml',
    ],
}
