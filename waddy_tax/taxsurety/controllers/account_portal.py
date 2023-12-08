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
from odoo import http, _
from odoo.exceptions import ValidationError
from odoo.addons.account.controllers.portal import PortalAccount
from odoo.addons.account_payment.controllers.payment import PaymentPortal
from odoo.exceptions import AccessError, MissingError
from odoo.http import request, route


class TaxsuretyDownpayment(PortalAccount):
    """
    This class contains the downpayment related
    Controllers.
    """

    @http.route(['/downpayment/my/invoices/<int:invoice_id>'], type='http',
                auth="public", website=True)
    def initiate_downpayment(self, invoice_id, access_token=None, **kw):
        """
        :param invoice_id: contains current id of invoice
        :param access_token: contains access
        token created from invoice.get_portal_url()
        :param kw: kw contains arguments from form.
        :return: redirect invoice.get_portal_url() to reload invoice
        """
        try:
            invoice_sudo = self._document_check_access('account.move',
                                                       invoice_id, access_token)
            if kw.get('is_down_payment') == 'True':
                invoice_sudo.write({
                    'is_downpayment': True,
                    'down_payment_amount': kw.get('down_payment_amount')
                })
            elif kw.get('is_down_payment') == 'False':
                invoice_sudo.write({
                    'is_downpayment': False,
                    'down_payment_amount': 0.00
                })
            return request.redirect(invoice_sudo.get_portal_url())
        except (AccessError, MissingError):
            return request.redirect('/my')

    def _invoice_get_page_view_values(self, invoice, access_token, **kwargs):
        """
        Super to add is downpayment and downpayment amount
        to the invoice rendered in website.
        :param invoice:
        :param access_token:
        :param kwargs:
        :return:
        """
        values = super()._invoice_get_page_view_values(invoice, access_token, **kwargs)
        if request.website.is_customer_downpayment_enabled:
            values.update({
                'amount': invoice.down_payment_amount if invoice.is_downpayment else invoice.amount_residual,
                'is_down_payment': invoice.is_downpayment,
                'down_payment_amount': invoice.down_payment_amount
            })
        return values


class TaxsuretyPayment(PaymentPortal):

    @route()
    def invoice_transaction(self, invoice_id, access_token, **kwargs):
        """
        Clear is_downpayment and down_payment_amount after payment.
        :param invoice_id:
        :param access_token:
        :param kwargs:
        :return:
        """
        try:
            invoice_sudo = self._document_check_access('account.move',
                                                       invoice_id,
                                                       access_token)
            invoice_sudo.write({
                'is_downpayment': False,
                'down_payment_amount': 0.0
            })
        except MissingError as error:
            raise error
        except AccessError:
            raise ValidationError(_("The access token is invalid."))
        return super().invoice_transaction(invoice_id, access_token,
                                                       **kwargs)
