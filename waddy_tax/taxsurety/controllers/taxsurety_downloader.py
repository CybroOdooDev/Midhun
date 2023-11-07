# -*- coding: utf-8 -*-
import base64
from odoo import http, _
from odoo.http import request

from odoo.exceptions import AccessError
from werkzeug.exceptions import NotFound


class TaxSuretyDownloader(http.Controller):

    @http.route(['/web/taxsurety',
        '/web/taxsurety/<string:xmlid>',
        '/web/taxsurety/<string:xmlid>/<string:filename>',
        '/web/taxsurety/<int:id>',
        '/web/taxsurety/<int:id>/<string:filename>',
        '/web/taxsurety/<string:model>/<int:id>/<string:field>',
        '/web/taxsurety/<string:model>/<int:id>/<string:field>/<string:filename>'],
        type='http', auth="user", website=True)
    def taxsurety_downloader(self, id=None):
        document = request.env['documents.document'].sudo().browse(id)
        user = request.env.user
        if not document:
            raise NotFound()
        if document.owner_id.id != user.id and \
                document.partner_id.id != user.partner_id.id \
                and user.partner_id.id not in document.message_follower_ids.partner_id.ids:
            raise AccessError(
                _("Sorry you are not allowed to access this document"))
        else:
            attachment = document.attachment_id
            attachment.public = True
            body = _('%s downloaded the document.', user.name)
            document.message_post(body=body, message_type='email',
                                  partner_ids=document.message_follower_ids.partner_id.ids)
            return request.redirect('/web/content/%s?download=true' % (
                attachment.id))

    @http.route(['/my/documents/upload'], type='http',
                auth="user", website=True, csrf=False)
    def documents_upload(self, **post):
        if post.get('document_id'):
            document = request.env['documents.document'].sudo().browse(
                int(post.get('document_id')))
            baseto64 = base64.b64encode(post.get(
                'doc_uploaded').read())
            attachment = request.env['ir.attachment'].sudo().create({
                'name': post.get('file_name'),
                'website_id': request.website.id,
                'key': post.get('file_name'),
                'datas': baseto64,
                'type': 'binary',
                'mimetype': post.get('file_type'),
                'public': True,
                'res_model': 'documents.document',
                'res_field': 'attachment_id',
                'res_id': document.id,
                'res_name': post.get('doc_uploaded'),
            })
            partners = request.env.user.sudo().partner_id.ids + request.env.ref(
                'taxsurety.group_taxsurety_tax_administrators').sudo().users.partner_id.ids
            document.attachment_id = attachment.id
            body = _('%s uploaded the document.', request.env.user.name)
            document.message_post(body=body, message_type='email',
                                  partner_ids=partners)
        return request.redirect('/my/documents')

    @http.route(['/my/documents/create_workspace'], type='http',
                auth="user", website=True, csrf=False)
    def documents_create_workspace(self, **post):
        if post.get('workspace_name'):
            last_name_alphabet = request.env.user.name.split()[-1][0].upper()
            tax_preparation_customers_workspace = request.env[
                'documents.folder'].sudo().search([
                    ('name', '=', 'Tax Preparation Customers')], limit=1)
            user_folder = request.env['documents.folder'].sudo().search([
                ('name', '=', request.env.user.name),
                ('parent_folder_id.name', '=', request.env.user.name.split()[-1][0])
            ], limit=1)
            if not user_folder:
                last_name_alphabet_folder = request.env['documents.folder'].sudo().search([
                    ('name', '=', last_name_alphabet),
                    ('parent_folder_id.name', '=', 'Tax Preparation Customers')
                ], limit=1)
                if not last_name_alphabet_folder:
                    if not tax_preparation_customers_workspace:
                        tax_preparation_customers_workspace = request.env[
                            'documents.folder'].with_context(
                            mail_create_nosubscribe=True).sudo().create({
                                'name': 'Tax Preparation Customers'
                            })
                    last_name_alphabet_folder = request.env[
                        'documents.folder'].with_context(
                        mail_create_nosubscribe=True).sudo().create({
                            'name': last_name_alphabet,
                            'parent_folder_id': tax_preparation_customers_workspace.id
                        })
                user_folder = request.env['documents.folder'].with_context(
                    mail_create_nosubscribe=True).sudo().create({
                    'name': request.env.user.name,
                    'parent_folder_id': last_name_alphabet_folder.id
                })
            folder = request.env['documents.folder'].sudo().create({
                'name': post.get('workspace_name'),
                'company_id': request.env.company.id,
                'parent_folder_id': user_folder.id
            })
            partners = request.env.user.sudo().partner_id.ids + request.env.ref(
                'taxsurety.group_taxsurety_tax_administrators').sudo().users.partner_id.ids
            folder.message_subscribe(
                partner_ids=partners)
            body = _('%s created a workspace.', request.env.user.name)
            folder.message_post(body=body, message_type='email',
                                partner_ids=partners)
        return request.redirect('/my/documents/')

    @http.route(['/my/documents/folder/document/upload'], type='http',
                auth="user", website=True, csrf=False)
    def documents_upload_to_workspace(self, **post):
        if post.get('folder_document_id') and post.get('doc_uploaded'):
            baseto64 = base64.b64encode(post.get(
                'doc_uploaded').read())
            attachment = request.env['ir.attachment'].sudo().create({
                'name': post.get('file_name')
                if post.get('file_name') else 'Unsupported File',
                'website_id': request.website.id,
                'key': post.get('file_name'),
                'datas': baseto64,
                'type': 'binary',
                'mimetype': post.get('file_type'),
                'public': True,
                'res_name': post.get('doc_uploaded'),
            })
            document = request.env['documents.document'].with_context(
                partner_id=request.env.user.partner_id).sudo().create({
                    'attachment_id': attachment.id,
                    'folder_id': int(post.get('folder_document_id')),
                })
            partners = request.env.ref(
                'taxsurety.group_taxsurety_tax_administrators').sudo().users.partner_id.ids
            document.message_subscribe(
                partner_ids=partners)
            body = _('%s uploaded a document.', request.env.user.name)
            document.message_post(body=body, message_type='email',
                                  partner_ids=document.message_follower_ids.partner_id.ids)
            return request.redirect('/my/documents/')

    @http.route(['/my/documents/folder/edit'], type='http',
                auth="user", website=True, csrf=False)
    def documents_edit_workspace(self, **post):
        if post.get('workspace_id'):
            workspace = request.env['documents.folder'].sudo().browse(
                int(post.get('workspace_id')))
            workspace.write({
                'name': post.get('workspace_name'),
            })
        return request.redirect('/my/documents')


