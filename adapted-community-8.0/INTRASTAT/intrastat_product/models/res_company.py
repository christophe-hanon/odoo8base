# -*- encoding: utf-8 -*-
##############################################################################
#
#    Intrastat Product module for Odoo
#    Copyright (C) 2011-2015 Akretion (http://www.akretion.com)
#    Copyright (C) 2009-2015 Noviat (http://www.noviat.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#    @author Luc de Meyer <info@noviat.com>
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

from openerp import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    intrastat_incoterm_id = fields.Many2one(
        'stock.incoterms',
        string='Default Incoterm for Intrastat',
        help="International Commercial Terms are a series of "
             "predefined commercial terms used in international "
             "transactions.")
    intrastat_arrivals = fields.Selection(
        '_intrastat_arrivals', string='Arrivals',
        default='extended', required=True)
    intrastat_dispatches = fields.Selection(
        '_intrastat_arrivals', string='Dispatches',
        default='extended', required=True)
    intrastat_transport_id = fields.Many2one(
        'intrastat.transport_mode',
        string='Default Transport Mode', ondelete='restrict')
    intrastat = fields.Char(
        string='Intrastat Declaration', store=True, readonly=True,
        compute='_compute_intrastat')
    intrastat_region_id = fields.Many2one(
        'intrastat.region',
        string='Default Intrastat Region')

    @api.model
    def _intrastat_arrivals(self):
        return [
            ('exempt', 'Exempt'),
            ('standard', 'Standard'),
            ('extended', 'Extended')]

    @api.model
    def _intrastat_dispatches(self):
        return [
            ('exempt', 'Exempt'),
            ('standard', 'Standard'),
            ('extended', 'Extended')]

    @api.one
    @api.depends('intrastat_arrivals', 'intrastat_dispatches')
    def _compute_intrastat(self):
        if self.intrastat_arrivals == 'exempt' \
                and self.intrastat_dispatches == 'exempt':
            self.intrastat = 'exempt'
        elif self.intrastat_arrivals == 'extended' \
                or self.intrastat_dispatches == 'extended':
            self.intrastat = 'extended'
        else:
            self.intrastat = 'standard'
