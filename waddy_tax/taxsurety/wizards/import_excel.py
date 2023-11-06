# -*- coding: utf-8 -*-
import base64
import xlrd
import logging
from odoo import fields, models
from odoo.exceptions import UserError
logger = logging.getLogger(__name__)


class PartnerMatching(models.TransientModel):
    _name = "partner.matching.wizard"
    _description = 'Partner Matching Wizard'

    contact_file = fields.Binary(
        string='Contact File')
    file_name = fields.Char(
        string='File Name')

    def regenerate_partners(self):
        try:
            book = xlrd.open_workbook(
                file_contents=(base64.decodebytes(self.contact_file)))
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')
        for sheet in book.sheets():
            for row in range(sheet.nrows):
                try:
                    if row >= 1:
                        row_values = sheet.row_values(row)
                        if row_values[8]:
                            partner = self.env['res.partner'].sudo().search([
                                '&',
                                ('email', '=ilike', row_values[8]),
                                ('name', '=ilike', row_values[1])
                            ])

                            state = self.env['res.country.state'].sudo().search([
                                ('code', '=', row_values[5]),
                                ('country_id.code', '=', 'US')
                            ], limit=1)

                            if partner:
                                for rec in partner:
                                    rec.write({
                                        'name': row_values[1],
                                        'vat': "{:04d}".format(int(row_values[0]))
                                    })
                            else:
                                partner = self.env['res.partner'].sudo().create({
                                    'company_type': 'person',
                                    'name': row_values[1],
                                    'email': row_values[8],
                                    'vat': "{:04d}".format(int(row_values[0])),
                                    'street': str(int(row_values[3])) if isinstance(row_values[3], float) else str(row_values[3]),
                                    'city': row_values[4],
                                    'state_id': state.id,
                                    'zip': str(int(row_values[6])) if isinstance(row_values[3], float) else row_values[6],
                                })
                                partner.street2 = row_values[2]
                        else:
                            state = self.env['res.country.state'].sudo().search(
                                [
                                    ('code', '=', row_values[5]),
                                    ('country_id.code', '=', 'US')
                                ], limit=1)

                            partner = self.env['res.partner'].sudo().search([
                                ('name', '=ilike', row_values[1]),
                            ])

                            if partner:
                                for rec in partner:
                                    rec.name = row_values[1]
                                    rec.vat = "{:04d}".format(int(row_values[0]))

                            else:
                                partner = self.env['res.partner'].sudo().create(
                                {
                                    'company_type': 'person',
                                    'name': row_values[1],
                                    'email': '',
                                    'vat': "{:04d}".format(
                                        int(row_values[0])),
                                    'street': str(
                                        int(row_values[3])) if isinstance(
                                        row_values[3], float) else str(
                                        row_values[3]),
                                    'city': row_values[4],
                                    'state_id': state.id,
                                    'zip': str(
                                        int(row_values[6])) if isinstance(
                                        row_values[3], float) else
                                    row_values[6],
                                })
                                partner.street2 = row_values[2]
                except Exception as e:
                    logger.warning(e)
