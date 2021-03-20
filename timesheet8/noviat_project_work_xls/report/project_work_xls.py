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
#    GNU Affero General Public License for more detptws.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import _
from openerp.tools.translate import translate
from openerp.report import report_sxw
from openerp.addons.report_xls.report_xls import report_xls
from openerp.addons.report_xls.utils import _render  # ,rowcol_to_cell
from datetime import datetime
import xlwt
# import logging
# _logger = logging.getLogger(__name__)


class project_work_xls_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, parents=None, tag=None, context=None):
        super(project_work_xls_parser, self).__init__(
            cr, uid, name, parents=parents, tag=tag, context=context)
        self.localcontext.update({
            'datetime': datetime,
            'get_selection_label': self._get_selection_label,
            '_': self._,
        })
        itn = __name__.split('openerp.')[1]
        self._ir_translation_name = itn.replace('.', '/') + '.py'
        self.context = context

    def _get_selection_label(self, object, field, val, context=None):
        if not context:
            context = self.context
        field_dict = self.pool[object._name].fields_get(
            self.cr, self.uid, allfields=[field],
            context=context)
        result_list = field_dict[field]['selection']
        result = filter(lambda x: x[0] == val, result_list)[0][1]
        return result

    def _(self, src, type='code'):
        lang = self.localcontext.get('lang', 'en_US')
        return translate(self.cr, self._ir_translation_name,
                         type, lang, src) or src


class project_work_xls(report_xls):

    def __init__(self, name, table, rml=False, parser=False, header=False,
                 store=False, register=True):
        super(project_work_xls, self).__init__(
            name, table, rml=rml, parser=parser, header=header,
            store=store, register=register)

        date_time_format = 'YYYY-MM-DD HH:MM'
        percentage_format = '0%'

        # Cell Styles
        _xs = self.xls_styles
        # header
        rh_cell_format = _xs['bold'] + _xs['fill'] + _xs['borders_all']
        self.rh_cell_style = xlwt.easyxf(rh_cell_format)
        self.rh_cell_style_center = xlwt.easyxf(rh_cell_format + _xs['center'])
        self.rh_cell_style_right = xlwt.easyxf(rh_cell_format + _xs['right'])
        # lines
        rl_cell_format = _xs['borders_all']
        self.rl_cell_style = xlwt.easyxf(rl_cell_format)
        self.rl_cell_style_center = xlwt.easyxf(rl_cell_format + _xs['center'])
        self.rl_cell_style_date_time = xlwt.easyxf(
            rl_cell_format + _xs['left'],
            num_format_str=date_time_format)
        self.rl_cell_style_decimal = xlwt.easyxf(
            rl_cell_format + _xs['right'],
            num_format_str=report_xls.decimal_format)
        self.rl_cell_style_decimal_center = xlwt.easyxf(
            rl_cell_format + _xs['center'],
            num_format_str=report_xls.decimal_format)
        self.rl_cell_style_percentage = xlwt.easyxf(
            rl_cell_format + _xs['right'],
            num_format_str=percentage_format)
        # totals
        rt_cell_format = _xs['bold'] + _xs['fill'] + _xs['borders_all']
        self.rt_cell_style = xlwt.easyxf(rt_cell_format)
        self.rt_cell_style_right = xlwt.easyxf(rt_cell_format + _xs['right'])
        self.rt_cell_style_decimal = xlwt.easyxf(
            rt_cell_format + _xs['right'],
            num_format_str=report_xls.decimal_format)

        # wanted list
        self.wanted_list = [
            'partner', 'start', 'task', 'name', 'travel', 'user', 'hours',
            'invoice_type', 'invoice_state', 'rate_multiplier'
        ]

        # XLS Template
        self.col_specs_template = {
            'partner': {
                'header': [1, 20, 'text', _render("_('Partner')")],
                'lines': [1, 0, 'text', _render("line.partner_id.name or ''")]
                },
            'start': {
                'header': [1, 18, 'text', _render("_('Started At')")],
                'lines': [
                    1, 0, 'date', _render(
                        "datetime.strptime(line.started_at,"
                        " '%Y-%m-%d %H:%M:%S')"),
                    None, self.rl_cell_style_date_time],
                },
            'task': {
                'header': [1, 40, 'text', _render("_('Task')")],
                'lines': [1, 0, 'text', _render("line.task_id.name or ''")]
                },
            'name': {
                'header': [1, 50, 'text', _render("_('Work summary')")],
                'lines': [1, 0, 'text', _render("line.name or ''")]
                },
            'travel': {
                'header': [
                    1, 10, 'text', _render("_('Travel')"),
                    None, self.rh_cell_style_center],
                'lines':
                    [1, 0, 'text',
                     _render("line.travel and 'x' or ''"),
                     None, self.rl_cell_style_center]
                },
            'user': {
                'header': [1, 16, 'text', _render("_('Done by')")],
                'lines': [1, 0, 'text', _render("line.user_id.name or ''")]
                },
            'hours': {
                'header': [
                    1, 12, 'text', _render("_('Time Spent')"),
                    None, self.rh_cell_style_center],
                'lines': [
                    1, 0, 'number',
                    _render("line.hours or 0.0"),
                    None, self.rl_cell_style_decimal_center]
                },
            'invoice_type': {
                'header': [1, 24, 'text', _render("_('Invoicing Agreement')")],
                'lines': [
                    1, 0, 'text', _render(
                        "get_selection_label(line, 'invoice_type',"
                        " line.invoice_type)")
                    ]
                },
            'invoice_state': {
                'header': [1, 24, 'text', _render("_('Invoicing State')")],
                'lines': [
                    1, 0, 'text', _render(
                        "get_selection_label(line, 'invoice_state',"
                        " line.invoice_state)")
                    ]
                },
            'rate_multiplier': {
                'header': [1, 14, 'text', _render("_('Billing Rate %')")],
                'lines': [
                    1, 0, 'number', _render(
                        "line.rate_multiplier and"
                        " float(line.rate_multiplier) or 1"),
                    None, self.rl_cell_style_percentage],
                },
        }

    def generate_xls_report(self, _p, _xs, data, objects, wb):

        report_name = _("Project Task Work overview")
        ws = wb.add_sheet(report_name[:31])
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0  # Landscape
        ws.fit_width_to_pages = 1
        row_pos = 0

        # set print header/footer
        ws.header_str = self.xls_headers['standard']
        ws.footer_str = self.xls_footers['standard']

        # Title
        cell_style = xlwt.easyxf(_xs['xls_title'])
        c_specs = [
            ('report_name', 1, 0, 'text', report_name),
        ]
        row_data = self.xls_row_template(c_specs, ['report_name'])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)
        row_pos += 1

        # Column headers
        c_specs = map(
            lambda x: self.render(
                x, self.col_specs_template, 'header',
                render_space={'_': _p._}),
            self.wanted_list)
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=self.rh_cell_style,
            set_column_size=True)
        ws.set_horz_split_pos(row_pos)
        ws.set_vert_split_pos(1)

        # lines
        for line in objects:
            c_specs = map(
                lambda x: self.render(x, self.col_specs_template, 'lines'),
                self.wanted_list)
            row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
            row_pos = self.xls_write_row(
                ws, row_pos, row_data, row_style=self.rl_cell_style)


project_work_xls(
    'report.project.work.xls',
    'project.task.work',
    parser=project_work_xls_parser)
