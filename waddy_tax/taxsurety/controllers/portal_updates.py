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
from odoo.http import request


class PortalUpdates(http.Controller):
    @http.route(['/my/contacts/update'], type='http',
                auth="user", website=True, csrf=False)
    def contacts_update(self, **post):
        if post.get('field_name') and post.get('description'):
            partner = request.env.user.partner_id
            body = _('Update for ' + post.get(
                'field_name') + ': ' + post.get(
                'description'))
            partners = request.env.ref(
                'taxsurety.group_taxsurety_tax_administrators').sudo().users.partner_id.ids
            partner.with_context(
                mail_create_nosubscribe=True).message_post(subject=_(
                    'Update for ' + post.get('field_name') + ' of ' + partner.name),
                body=body, message_type='email', partner_ids=partners)
        return request.redirect('/my/home')

    @http.route(['/my/contacts/bank_and_cc_update'], type='http',
                auth="user", website=True, csrf=False)
    def bank_and_cc_update(self, **post):
        if post.get('field_name') and post.get('bank_and_cc'):
            request.env.user.partner_id.write(
                {post.get('field_name'): post.get('bank_and_cc')}
            )
        return request.redirect('/my/home')

    @http.route(['/my/contacts/cc_expiration_update'], type='http',
                auth="user", website=True, csrf=False)
    def cc_expiration_update(self, **post):
        date = post.get('cc_month_year').split("-")
        year = date[0]
        month = int(date[1])
        request.env.user.partner_id.write({
            'cc_exp_date_month': str(month),
            'cc_exp_date_year': str(year),
        })
        return request.redirect('/my/home')

#     Delete workspace
    @http.route(['/my/documents_workspace/delete'], type='http',
                auth="user", website=True, csrf=False)
    def delete_workspace(self, **post):
        if post.get('document_workspace_id'):
            document_workspace = request.env[
                'documents.folder'].sudo().browse(
                    int(post.get('document_workspace_id')))
            if document_workspace:
                document_workspace.unlink()
        return request.redirect('/my/documents')

# ---- Change workspace of document
    @http.route(['/my/documents/folder/change'], type='http',
                auth='user', website=True, csrf=False)
    def folder_change(self, **post):
        if post.get('document_id') and post.get('folder_id'):
            document = request.env['documents.document'].sudo().browse(
                int(post.get('document_id')))
            workspace = request.env['documents.folder'].sudo().browse(
                int(post.get('folder_id')))
            document.folder_id = workspace.id
            return request.redirect('/my/documents/%s' % document.id)
