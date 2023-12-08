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

from odoo import models, fields, _
from werkzeug.urls import url_join, url_quote
from odoo.tools import config, get_lang, is_html_empty, formataddr, groupby, format_date


class SignRequest(models.Model):
    _inherit = "sign.request"

    message = fields.Html(string="Message",
                          translate=True,
                          prefetch=True,
                          sanitize=False,
                          help="Message to be sent to signers"
                               " of the specified document")

    email_template_id = fields.Many2one(
        comodel_name='mail.template',
        string="Email Template",
        domain="[('model_id.model', '=', 'res.partner')]",
        ondelete='cascade')


class SignRequestItem(models.Model):
    _inherit = "sign.request.item"

    def _send_signature_access_mail(self):
        """
        For signers if mail template is present:
        :return: Nothing
        """
        for signer in self:
            mail_template = signer.sign_request_id.email_template_id
            mail_subject = ''
            if mail_template:
                sent_mail_id = mail_template.send_mail(signer.partner_id.id,
                                                       force_send=False)
                send_mail = self.env['mail.mail'].browse(sent_mail_id)
                mail_body = send_mail.body
                mail_subject = send_mail.subject
                send_mail.unlink()
                signer_lang = get_lang(self.env, lang_code=signer.partner_id.lang).code
                context = {'lang': signer_lang}
                body = self.env['ir.qweb']._render('sign.sign_template_mail_request', {
                    'record': signer,
                    'link': url_join(signer.get_base_url(), "sign/document/mail/%(request_id)s/%(access_token)s" % {'request_id': signer.sign_request_id.id, 'access_token': signer.sudo().access_token}),
                    'subject': mail_subject,
                    'body': mail_body if not is_html_empty(signer.sign_request_id.message) else False,
                    'use_sign_terms': self.env['ir.config_parameter'].sudo().get_param('sign.use_sign_terms'),
                    'user_signature': signer.create_uid.signature,
                }, lang=signer_lang, minimal_qcontext=True)
                attachment_ids = signer.sign_request_id.attachment_ids.ids
            else:
                signer_lang = get_lang(self.env,
                                       lang_code=signer.partner_id.lang).code
                context = {'lang': signer_lang}
                body = self.env['ir.qweb']._render(
                    'sign.sign_template_mail_request', {
                        'record': signer,
                        'link': url_join(signer.get_base_url(),
                                         "sign/document/mail/%(request_id)s/%(access_token)s" % {
                                             'request_id': signer.sign_request_id.id,
                                             'access_token': signer.sudo().access_token}),
                        'subject': signer.sign_request_id.subject,
                        'body': signer.sign_request_id.message if not is_html_empty(
                            signer.sign_request_id.message) else False,
                        'use_sign_terms': self.env[
                            'ir.config_parameter'].sudo().get_param(
                            'sign.use_sign_terms'),
                        'user_signature': signer.create_uid.signature,
                    }, lang=signer_lang, minimal_qcontext=True)
                attachment_ids = signer.sign_request_id.attachment_ids.ids
            self.env['sign.request']._message_send_mail(
                body, 'mail.mail_notification_light',
                {'record_name': signer.sign_request_id.reference},
                {'model_description': _('Signature'), 'company': signer.communication_company_id or signer.sign_request_id.create_uid.company_id},
                {'email_from': signer.create_uid.email_formatted,
                 'author_id': signer.create_uid.partner_id.id,
                 'email_to': formataddr((signer.partner_id.name, signer.signer_email)),
                 'attachment_ids': attachment_ids,
                 'subject': mail_subject if mail_subject != '' else signer.sign_request_id.subject},
                force_send=True,
                lang=signer_lang,
            )
            signer.is_mail_sent = True
            del context
