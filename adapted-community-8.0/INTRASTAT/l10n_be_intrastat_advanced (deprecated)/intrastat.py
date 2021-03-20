# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 Noviat nv/sa (www.noviat.com).
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

from openerp import models, fields, api


class intrastat_region(models.Model):
    _name = 'intrastat.region'
    _description = "Intrastat Region"

    @api.model
    def _get_company(self):
        return self.env['res.company']._company_default_get('account.account')

    code = fields.Char(string='Code', required=True)
    country_id = fields.Many2one('res.country', string='Country', required=True)
    name = fields.Char(string='Name', translate=True)
    description = fields.Char(string='Description')
    company_id = fields.Many2one(
        'res.company', string='Company', default=_get_company)

    _sql_constraints = [
        ('intrastat_region_code_unique', 
         'UNIQUE(code, country_id)', 
         'Code must be unique.')]


class intrastat_transaction(models.Model):
    _name = 'intrastat.transaction'
    _description = "Intrastat Transaction"
    _order = 'code'
    _rec_name = "display_name"

    @api.model
    def _get_company(self):
        return self.env['res.company']._company_default_get('account.account')

    @api.one
    @api.depends('code', 'description')
    def _compute_display_name(self):
        display_name = self.code
        if self.description:
            display_name += ' ' + self.description
        self.display_name = display_name > 55 \
            and display_name[:55] + '...' \
            or display_name

    code = fields.Char(string='Code', required=True)
    description = fields.Text(string='Description')
    display_name = fields.Char(
        compute='_compute_display_name', string="Display Name", readonly=True)
    company_id = fields.Many2one(
        'res.company', string='Company', default=_get_company)

    _sql_constraints = [
        ('intrastat_transaction_code_unique', 
         'UNIQUE(code)', 
         'Code must be unique.')]


class intrastat_transport_mode(models.Model):
    _name = 'intrastat.transport_mode'
    _description = "Intrastat Transport Mode"

    @api.model
    def _get_company(self):
        return self.env['res.company']._company_default_get('account.account')

    code = fields.Char(string='Code', required=True)
    name = fields.Char('Description')
    company_id = fields.Many2one(
        'res.company', string='Company', default=_get_company)

    _sql_constraints = [
        ('intrastat_transport_code_unique', 
         'UNIQUE(code)', 
         'Code must be unique.')]

class intrastat_result_view(models.TransientModel):
    """
    Transient Model to display Intrastat Report results
    """
    _name = 'intrastat.result.view'

    note = fields.Text(
        string='Notes', readonly=True,
        default=lambda self: self._context.get('note'))
