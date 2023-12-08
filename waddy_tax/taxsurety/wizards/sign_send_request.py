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
#s
########################################################################################

from odoo import fields, models, Command


class SignSendRequest(models.TransientModel):
    _inherit = 'sign.send.request'

    email_template_id = fields.Many2one(
        comodel_name='mail.template',
        string="Email Template",
        domain="[('model_id.model', '=', 'res.partner')]",
        ondelete='cascade')

    subject = fields.Char(string="Subject",
                          required=True,
                          store=True,
                          readonly=False,
                          related='email_template_id.subject')

    model_id = fields.Many2one(
        comodel_name='ir.model',
        related='email_template_id.model_id')

    message = fields.Html(string="Message",
                          translate=True,
                          prefetch=True,
                          store=True,
                          related="email_template_id.body_html",
                          readonly=False,
                          sanitize=False,
                          help="Message to be sent to signers"
                               " of the specified document")

    def create_request(self):
        """
        over write to add email template from
        sign.send.request
        and add sgn request to document workspace
        :return: sign_request
        """
        template_id = self.template_id.id
        if self.signers_count:
            signers = [{'partner_id': signer.partner_id.id,
                        'role_id': signer.role_id.id,
                        'mail_sent_order': signer.mail_sent_order} for signer in
                       self.signer_ids]
        else:
            signers = [{'partner_id': self.signer_id.id,
                        'role_id': self.env.ref(
                            'sign.sign_item_role_default').id,
                        'mail_sent_order': self.signer_ids.mail_sent_order}]
        cc_partner_ids = self.cc_partner_ids.ids
        reference = self.filename
        subject = self.subject
        message = self.message
        message_cc = self.message_cc
        attachment_ids = self.attachment_ids
        refusal_allowed = self.refusal_allowed
        sign_request = self.env['sign.request'].create({
            'template_id': template_id,
            'email_template_id': self.email_template_id.id,
            'request_item_ids': [Command.create({
                'partner_id': signer['partner_id'],
                'role_id': signer['role_id'],
                'mail_sent_order': signer['mail_sent_order'],
            }) for signer in signers],
            'reference': reference,
            'subject': subject,
            'message': message,
            'message_cc': message_cc,
            'attachment_ids': [Command.set(attachment_ids.ids)],
            'refusal_allowed': refusal_allowed,
        })
        sign_request.message_subscribe(partner_ids=cc_partner_ids)
        for rec in sign_request.request_item_ids:
            last_name_alphabet = rec.partner_id.name.split()[-1][0].upper()
            f_and_l_name = rec.partner_id.name.split()
            l_name = f_and_l_name[-1]
            f_name = ' '.join([str(name) for name in f_and_l_name[:-1]])
            if len(f_and_l_name) > 1:
                doc_name = l_name + ', ' + f_name
            else:
                doc_name = l_name
            tax_preparation_customers_workspace = self.env[
                'documents.folder'].sudo().search([
                    ('name', '=', 'Tax Preparation Customers')],
                limit=1)
            user_folder = self.env['documents.folder'].sudo().search([
                ('name', '=', doc_name),
                ('parent_folder_id.name', '=',
                 rec.partner_id.name.split()[-1][0].upper())],
                limit=1)
            if not user_folder:
                last_name_alphabet_folder = self.env[
                    'documents.folder'].sudo().search([
                        ('name', '=', last_name_alphabet),
                        ('parent_folder_id.name', '=',
                         'Tax Preparation Customers')
                    ], limit=1)
                if not last_name_alphabet_folder:
                    if not tax_preparation_customers_workspace:
                        tax_preparation_customers_workspace = self.env[
                            'documents.folder'].with_context(
                            mail_create_nosubscribe=True).sudo().create({
                                'name': 'Tax Preparation Customers'
                            })
                    last_name_alphabet_folder = self.env[
                        'documents.folder'].with_context(
                        mail_create_nosubscribe=True).sudo().create({
                            'name': last_name_alphabet,
                            'parent_folder_id': tax_preparation_customers_workspace.id
                        })
                user_folder = self.env['documents.folder'].with_context(
                    mail_create_nosubscribe=True).sudo().create({
                        'name': doc_name,
                        'parent_folder_id': last_name_alphabet_folder.id
                    })
            signature_request_folder = self.env['documents.folder'].sudo().search([
                ('name', '=', 'Signature Requests'),
                ('parent_folder_id', '=',
                 user_folder.id)],
                limit=1)
            if not signature_request_folder:
                signature_request_folder = self.env['documents.folder'].sudo().create({
                    'name': 'Signature Requests',
                    'parent_folder_id': user_folder.id
                })
            document = self.env['documents.document'].sudo().create({
                'name': 'Signature Request: ' + sign_request.reference,
                'type': 'url',
                'folder_id': signature_request_folder.id,
                'partner_id': rec.partner_id.id,
                'url': '%s/my/signature/%s' % (self.get_base_url(), rec.id)
            })
        return sign_request
