# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#
#    Copyright (c) 2009-2015 Noviat nv/sa (www.noviat.com).
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

from openerp import models, fields, api, _
from openerp.exceptions import Warning

from lxml import etree
import logging
_logger = logging.getLogger(__name__)

_INTRASTAT_XMLNS = 'http://www.onegate.eu/2010-01-01'


class L10nBeIntrastatProductDeclaration(models.Model):
    _name = 'l10n.be.intrastat.product.declaration'
    _description = "Intrastat Product Declaration for Belgium"
    _inherit = ['intrastat.product.declaration', 'mail.thread']

    computation_line_ids = fields.One2many(
        'l10n.be.intrastat.product.computation.line',
        'parent_id', string='Intrastat Product Computation Lines',
        states={'done': [('readonly', True)]})
    declaration_line_ids = fields.One2many(
        'l10n.be.intrastat.product.declaration.line',
        'parent_id', string='Intrastat Product Declaration Lines',
        states={'done': [('readonly', True)]})

    def _get_region(self, inv_line):
        region = super(
            L10nBeIntrastatProductDeclaration, self)._get_region(inv_line)
        if not region:
            msg = _(
                "The Intrastat Region of the Company is not set, "
                "please configure it first.")
            self._company_warning(msg)
        return region

    def _update_computation_line_vals(self, inv_line, line_vals):
        if self.company_country_code == 'be':
            region = self._get_region(inv_line)
            line_vals.update({
                'region_id': region.id,
                })
            if self._extended and self.company_country_code == 'be':
                incoterm = self._get_incoterm(inv_line)
                line_vals.update({
                    'incoterm_id': incoterm.id,
                    })
        else:
            super(L10nBeIntrastatProductDeclaration, self
                  )._update_computation_line_vals(inv_line, line_vals)

    @api.one
    def _check_generate_xml(self):
        res = super(
            L10nBeIntrastatProductDeclaration, self)._check_generate_xml()
        if not self.declaration_line_ids:
            res = self.generate_declaration()
        kbo_nr = False
        if self.company_id.partner_id.registry_authority == 'kbo_bce':
            kbo_nr = self.company_id.partner_id.registry_number
        if not kbo_nr:
            raise Warning(
                _("Configuration Error."),
                _("No KBO/BCE Number defined for your Company."))
        return res

    def _node_Admininstration(self, parent):
        Administration = etree.SubElement(parent, 'Administration')
        From = etree.SubElement(Administration, 'From')
        From.text = self.company_id.partner_id.registry_number
        From.set('declarerType', 'KBO')
        etree.SubElement(Administration, 'To').text = "NBB"
        etree.SubElement(Administration, 'Domain').text = "SXX"

    def _node_Item(self, parent, line):
        Item = etree.SubElement(parent, 'Item')
        etree.SubElement(
            Item, 'Dim',
            attrib={'prop': 'EXTRF'}).text = self._decl_code
        etree.SubElement(
            Item, 'Dim',
            attrib={'prop': 'EXCNT'}
            ).text = line.src_dest_country_id.code
        etree.SubElement(
            Item, 'Dim',
            attrib={'prop': 'EXTTA'}
            ).text = line.transaction_id.code
        etree.SubElement(
            Item, 'Dim',
            attrib={'prop': 'EXREG'}
            ).text = line.region_id.code
        etree.SubElement(
            Item, 'Dim',
            attrib={'prop': 'EXTGO'}
            ).text = line.hs_code_id.local_code
        etree.SubElement(
            Item, 'Dim',
            attrib={'prop': 'EXWEIGHT'}
            ).text = str(line.weight)
        etree.SubElement(
            Item, 'Dim',
            attrib={'prop': 'EXUNITS'}
            ).text = str(line.suppl_unit_qty)
        etree.SubElement(
            Item, 'Dim',
            attrib={'prop': 'EXTXVAL'}
            ).text = str(line.amount_company_currency)
        if self.reporting_level == 'extended':
            etree.SubElement(
                Item, 'Dim',
                attrib={'prop': 'EXTPC'}
                ).text = line.transport_id.code
            etree.SubElement(
                Item, 'Dim',
                attrib={'prop': 'EXDELTRM'}
                ).text = line.incoterm_id.code

    def _node_Data(self, parent):
        Data = etree.SubElement(parent, 'Data')
        Data.set('close', 'true')
        report_form = 'EXF' + self._decl_code
        if self.reporting_level == 'standard':
            report_form += 'S'
        else:
            report_form += 'E'
        Data.set('form', report_form)
        if self.action != 'nihil':
            for line in self.declaration_line_ids:
                self._node_Item(Data, line)

    def _node_Report(self, parent):
        Report = etree.SubElement(parent, 'Report')
        Report.set('action', self.action)
        Report.set('date', self.year_month)
        report_code = 'EX' + self._decl_code
        if self.reporting_level == 'standard':
            report_code += 'S'
        else:
            report_code += 'E'
        Report.set('code', report_code)
        self._node_Data(Report)

    @api.multi
    def _generate_xml(self):

        if self.type == 'arrivals':
            self._decl_code = '19'
        else:
            self._decl_code = '29'

        ns_map = {
            None: _INTRASTAT_XMLNS,
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        }
        root = etree.Element('DeclarationReport', nsmap=ns_map)
        self._node_Admininstration(root)
        self._node_Report(root)

        xml_string = etree.tostring(
            root, pretty_print=True, encoding='UTF-8', xml_declaration=True)
        module = __name__.split('addons.')[1].split('.')[0]
        self._check_xml_schema(xml_string, '%s/data/onegate.xsd' % module)
        return xml_string


class L10nBeIntrastatProductComputationLine(models.Model):
    _name = 'l10n.be.intrastat.product.computation.line'
    _inherit = 'intrastat.product.computation.line'

    parent_id = fields.Many2one(
        'l10n.be.intrastat.product.declaration',
        string='Intrastat Product Declaration',
        ondelete='cascade', readonly=True)
    declaration_line_id = fields.Many2one(
        'l10n.be.intrastat.product.declaration.line',
        string='Declaration Line', readonly=True)


class L10nBeIntrastatProductDeclarationLine(models.Model):
    _name = 'l10n.be.intrastat.product.declaration.line'
    _inherit = 'intrastat.product.declaration.line'

    parent_id = fields.Many2one(
        'l10n.be.intrastat.product.declaration',
        string='Intrastat Product Declaration',
        ondelete='cascade', readonly=True)
    computation_line_ids = fields.One2many(
        'l10n.be.intrastat.product.computation.line', 'declaration_line_id',
        string='Computation Lines', readonly=True)

    @api.model
    def _group_line_hashcode_fields(self, computation_line):
        res = super(
            L10nBeIntrastatProductDeclarationLine, self
            )._group_line_hashcode_fields(computation_line)
        if self.company_id.country_id.code == 'BE':
            del res['product_origin_country']
        return res

    @api.model
    def _prepare_grouped_fields(self, computation_line, fields_to_sum):
        vals = super(
            L10nBeIntrastatProductDeclarationLine, self
            )._prepare_grouped_fields(computation_line, fields_to_sum)
        vals.update({
            'region_id': computation_line.region_id.id,
            })
        return vals
