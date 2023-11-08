# -*- coding: utf-8 -*-
from odoo import fields, models, _, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    etp_q1 = fields.Char(string="Q1",
                         help="Estimated Tax Payment Q1")
    etp_q2 = fields.Char(string="Q2",
                         help="Estimated Tax Payment Q2")
    etp_q3 = fields.Char(string="Q3",
                         help="Estimated Tax Payment Q3")
    etp_q4 = fields.Char(string="Q4",
                         help="Estimated Tax Payment Q4")
    est_savings = fields.Char(string="Annual Estimated Savings",
                              help="Annual Estimated Savings")

    bank_name = fields.Char(string="Bank name",
                            help="Bank name")
    bank_accnt_no = fields.Char(string="Bank account no.",
                                help="Bank account number")
    routing_no = fields.Char(string="Routing no.",
                             help="Routing number")

    cc_name = fields.Char(string="Credit card name",
                          help="Credit card name")
    cc_no = fields.Char(string="Credit card no.",
                        help="Credit card number")
    cc_code = fields.Char(string="Security code",
                          help="Security code")
    cc_exp_date_month = fields.Selection([('1', 'January'),
                                          ('2', 'February'),
                                          ('3', 'March'),
                                          ('4', 'April'),
                                          ('5', 'May'),
                                          ('6', 'June'),
                                          ('7', 'July'),
                                          ('8', 'August'),
                                          ('9', 'September'),
                                          ('10', 'October'),
                                          ('11', 'November'),
                                          ('12', 'December')],
                                         string="Expiration month",
                                         )
    cc_exp_date_year = fields.Char(string="Expiration year",
                                   help="Expiration year")

    def action_update_contacts_through_excel(self):
        return {
            'name': _("Import Contact"),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'partner.matching.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
