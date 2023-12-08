# -*- coding: utf-8 -*-
######################################################################################
#
#    Waddy Accounting Services
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Waddy Accounting Services
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################
import re
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'
    """
    Adding fields for taxsurety
    """

    first_name = fields.Char(string="First Name",
                             help="First name",
                             )
    last_name = fields.Char(string="Last Name",
                            help="Last name",
                            )

    etp_q1 = fields.Char(string="Q1",
                         help="Estimated Tax Payment Q1",
                         tracking=True)
    etp_q2 = fields.Char(string="Q2",
                         help="Estimated Tax Payment Q2",
                         tracking=True)
    etp_q3 = fields.Char(string="Q3",
                         help="Estimated Tax Payment Q3",
                         tracking=True)
    etp_q4 = fields.Char(string="Q4",
                         help="Estimated Tax Payment Q4",
                         tracking=True)
    est_savings = fields.Char(string="Annual Estimated Savings",
                              help="Annual Estimated Savings",
                              tracking=True)

    bank_name = fields.Char(string="Bank name",
                            help="Bank name",
                            tracking=True)
    bank_accnt_no = fields.Char(string="Bank account no.",
                                help="Bank account number",
                                tracking=True)
    routing_no = fields.Char(string="Routing no.",
                             help="Routing number",
                             tracking=True)

    cc_name = fields.Char(string="Credit card name",
                          help="Credit card name",
                          tracking=True)
    cc_no = fields.Char(string="Credit card no.",
                        help="Credit card number",
                        tracking=True)
    cc_code = fields.Char(string="Security code",
                          help="Security code",
                          tracking=True)
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
                                         tracking=True)
    cc_exp_date_year = fields.Char(string="Expiration year",
                                   help="Expiration year",
                                   tracking=True)

    federal_return_results = fields.Text(string="Federal return results",
                                         help="Federal return results",
                                         tracking=True)
    state_return_results = fields.Text(string="State return results",
                                       help="State return results",
                                       tracking=True)

    @api.model
    def message_new(self, msg, custom_values=None):
        """ Overrides mail_thread message_new that is called by the mailgateway
            through message_process.
            This override updates the document according to the email.
        """
        result = super(ResPartner, self).message_new(msg, custom_values=custom_values)
        if msg.get('subject') == 'Favorable Introduction':
            if msg.get('recipients'):
                emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", msg.get('recipients'))
                for rec in emails[:1]:
                    if not self.search([('email', '=', rec)]):
                        result.write({
                            'name': rec,
                            'email': rec,
                        })
                for rec in emails[1:]:
                    if not self.search([('email', '=', rec)]):
                        contact = result.copy()
                        contact.write({
                            'name': rec,
                            'email': rec,
                        })
        return result
