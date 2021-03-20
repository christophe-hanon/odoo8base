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

from openerp import models, fields, api


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def _default_intrastat_transaction(self):
        tr = self.env.ref(
                'l10n_be_intrastat_advanced.intrastat_transaction_1')
        return tr

    incoterm_id = fields.Many2one(
        'stock.incoterms', string='Incoterm',
        help="International Commercial Terms are a series of predefined "
             "commercial terms used in international transactions.")
    intrastat_transaction_id = fields.Many2one(
        'intrastat.transaction', string='Intrastat Transaction Type',
        default = _default_intrastat_transaction,
        help="Intrastat nature of transaction")
    transport_mode_id = fields.Many2one(
        'intrastat.transport_mode', string='Intrastat Transport Mode')
    intrastat_country_id = fields.Many2one(
        'res.country', string='Intrastat Country',
        help="Intrastat Partner Country, "
             "delivery for sales, origin for purchases",
        domain=[('intrastat', '=', True)])
    intrastat = fields.Char(string='Intrastat Declaration',
        related='company_id.intrastat',
        store=True, readonly=True)

    @api.multi
    def onchange_partner_id(self, type, partner_id, date_invoice=False,
            payment_term=False, partner_bank_id=False, company_id=False):
        res = super(account_invoice, self).onchange_partner_id(
            type, partner_id, date_invoice=date_invoice,
            payment_term=payment_term, partner_bank_id=partner_bank_id,
            company_id=company_id)
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            if partner.country_id.intrastat:
                res['value']['intrastat_country_id'] = partner.country_id.id
        return res


class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    intrastat_id = fields.Many2one(
        'report.intrastat.code', string='Intrastat Code')

    @api.multi
    def product_id_change(self, product, uom_id, qty=0, name='',
                          type='out_invoice', partner_id=False,
                          fposition_id=False, price_unit=False,
                          currency_id=False, company_id=None):
        res = super(account_invoice_line, self).product_id_change(
            product, uom_id, qty=qty, name=name, type=type,
            partner_id=partner_id, fposition_id=fposition_id,
            price_unit=price_unit, currency_id=currency_id,
            company_id=company_id)

        if product:
            pt = self.env['product.product'].browse(product).product_tmpl_id
            intrastat = pt.get_intrastat_recursively()
            if intrastat:
                res['value']['intrastat_id'] = intrastat.id

        return res