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

from odoo import http, _, SUPERUSER_ID
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from collections import OrderedDict
import base64
import json

from operator import itemgetter

from odoo.exceptions import AccessError, MissingError, UserError
from odoo.http import request
from odoo.tools import consteq
from odoo.tools import groupby as groupbyelem
from odoo.osv.expression import OR


class TaxSuretyPortal(CustomerPortal):

    def _doc_domain(self):
        return ['|', '|', '|', ('owner_id', '=', request.env.user.id),
                ('partner_id', '=', request.env.user.partner_id.id),
                ('folder_id.message_follower_ids.partner_id', 'in', request.env.user.partner_id.ids),
                ('message_follower_ids.partner_id',
                'in', request.env.user.partner_id.ids)]

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'document_count' in counters:
            document_count = request.env['documents.document'].sudo().search_count(
                self._doc_domain())
            values['document_count'] = document_count if document_count else 0
        return values

    def _get_my_documents_searchbar_filters(self, ):
        documents = request.env['documents.document'].sudo().search(
            self._doc_domain())
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }
        for rec in documents:
            for tag in rec.tag_ids:
                searchbar_filters.update({
                    str(tag.id): {'label': rec.folder_id.name + ': ' + tag.facet_id.name + ' > ' + tag.name,
                                  'domain': [('tag_ids', 'in', tag.ids)]}
                })
        return searchbar_filters

    @http.route(['/my/documents',
                 '/my/documents/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_my_docments(self, page=1, date_begin=None, date_end=None,
                           sortby=None, filterby=None, search=None,
                           search_in='all', groupby=None, **kw):

        if not filterby:
            filterby = 'all'
        searchbar_filters = self._get_my_documents_searchbar_filters()
        domain = searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']

        values = self._prepare_my_documents_values(
            page, date_begin, date_end, sortby, filterby,
            search, search_in, groupby, domain=domain)

        # pager
        pager_vals = values['pager']
        pager_vals['url_args'].update(filterby=filterby)
        pager = portal_pager(**pager_vals)

        # Documents that are created by user
        empty_document_folders = request.env['documents.folder'].sudo().search([
            ('message_follower_ids.partner_id',
             'in', request.env.user.partner_id.ids),
            ('document_ids', '=', False)],)

        # content according to pager and archive selected

        values.update({
            'grouped_documents': values['grouped_documents'](pager['offset']),
            'pager': pager,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'document_folders': empty_document_folders.sorted(key=lambda r: r.name.lower()),
        })
        return request.render("taxsurety.portal_my_documents", values)

    def _get_document_searchbar_sortings(self):
        return {
            'date': {'label': _('Date'), 'order': 'create_date desc', 'sequence': 1},
            'name': {'label': _('Name'), 'order': 'name asc', 'sequence': 2},
            'owner': {'label': _('Owner'), 'order': 'owner_id asc', 'sequence': 3},
            'contact': {'label': _('Contact'), 'order': 'partner_id asc', 'sequence': 4},
            'workspace': {'label': _('Workspace'), 'order': 'folder_id asc', 'sequence': 5}
        }

    def _document_get_searchbar_inputs(self):
        values = {
            'all': {'input': 'all', 'label': _('Search in All'), 'order': 1},
            'workspace': {'input': 'workspace', 'label': _('Search in Workspace'),
                          'order': 2},
            'owner': {'input': 'owner', 'label': _('Search in Owner'),
                      'order': 3},
            'contact': {'input': 'contact', 'label': _('Search in Contact'),
                        'order': 4},
        }
        return dict(sorted(values.items(), key=lambda item: item[1]["order"]))

    def _document_get_searchbar_groupby(self):
        values = {
            'none': {'input': 'none', 'label': _('None'), 'order': 1},
            'workspace': {'input': 'workspace', 'label': _('Workspace'), 'order': 2},
            'owner': {'input': 'owner', 'label': _('Owner'), 'order': 3},
            'contact': {'input': 'contact', 'label': _('Contact'), 'order': 4},
        }
        return dict(sorted(values.items(), key=lambda item: item[1]["order"]))

    def _document_get_search_domain(self, search_in, search):
        search_domain = []
        if search_in in ('all'):
            search_domain.append([('name', 'ilike', search)])
        if search_in in ('workspace', 'all'):
            search_domain.append([('folder_id', 'ilike', search)])
        if search_in in ('owner', 'all'):
            search_domain.append([('owner_id', 'ilike', search)])
        if search_in in ('contact', 'all'):
            search_domain.append([('partner_id', 'ilike', search)])
        return OR(search_domain)

    def _document_get_order(self, order, groupby):
        groupby_mapping = self._document_get_groupby_mapping()
        field_name = groupby_mapping.get(groupby, '')
        if not field_name:
            return order
        return '%s, %s' % (field_name, order)

    def _document_get_groupby_mapping(self):
        return {
            'workspace': 'folder_id',
            'owner': 'owner_id',
            'contact': 'partner_id',
        }

    def _prepare_my_documents_values(self, page, date_begin, date_end, sortby,
                                     filterby, search, search_in, groupby,
                                     domain=None, url="/my/documents"):
        values = self._prepare_portal_layout_values()
        Documents = request.env['documents.document']
        Documents_sudo = Documents.sudo()
        domain = expression.AND([
            domain or [],
            self._doc_domain(),
        ])

        searchbar_sortings = dict(sorted(
            self._get_document_searchbar_sortings().items(),
            key=lambda itm: itm[1]["sequence"]))

        searchbar_inputs = self._document_get_searchbar_inputs()
        searchbar_groupby = self._document_get_searchbar_groupby()

        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # default filter by value
        if not groupby:
            groupby = 'workspace'

        if not search_in:
            search_in = 'all'

        if search and search_in:
            domain += self._document_get_search_domain(search_in, search)

        order = self._document_get_order(order, groupby)

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        def get_grouped_documents(pager_offset):
            docs = Documents_sudo.search(domain, order=order, limit=self._items_per_page, offset=pager_offset)
            groupby_mapping = self._document_get_groupby_mapping()
            group = groupby_mapping.get(groupby)
            if group:
                grouped_documents = [Documents_sudo.concat(*g) for k, g in groupbyelem(docs, itemgetter(group))]
            else:
                grouped_documents = [docs] if docs else []
            return grouped_documents

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_documents': get_grouped_documents,
            'page_name': 'document',
            'pager': {  # vals to define the pager.
                "url": url,
                "url_args": {'date_begin': date_begin,
                             'date_end': date_end, 'sortby': sortby,
                             'groupby': groupby, 'search_in': search_in,
                             'total': Documents_sudo.search_count(domain),
                             'search': search},
                "total": Documents.sudo().search_count(domain),
                "page": page,
                "step": self._items_per_page,
            },
            'default_url': url,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_groupby': searchbar_groupby,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'groupby': groupby,
        })
        return values

    # Document full page
    @http.route(['/my/documents/<int:doc>'], type='http',
                auth='user', website=True)
    def portal_documents_view(self, **kw):
        document = request.env['documents.document'].sudo().browse(
            kw.get('doc'))
        user = request.env.user
        if document.owner_id.id != user.id and\
                document.partner_id.id != user.partner_id.id\
                and user.partner_id.id not in document.message_follower_ids.partner_id.ids\
                and not set(document.folder_id.message_follower_ids.partner_id.ids).intersection(set(request.env.user.partner_id.ids)):
            raise AccessError(
                _("Sorry you are not allowed to access this document"))
        else:
            workspace = request.env['documents.folder'].sudo()
            empty_document_folders = workspace.search([
                    ('message_follower_ids.partner_id',
                     'in', request.env.user.partner_id.ids)])
            documents = request.env['documents.document'].sudo().search([
                '|', '|', ('message_follower_ids.partner_id',
                           'in', request.env.user.partner_id.ids),
                          ('partner_id', '=', request.env.user.partner_id.id),
                          ('owner_id', '=', request.env.user.id)])
            folder_ids = list(set(
                empty_document_folders.ids + documents.folder_id.ids))
            workspaces = workspace.browse(folder_ids)
            return request.render('taxsurety.document_details',
                                  {'document': document,
                                   'page_name': 'document_details',
                                   'document_access': True,
                                   'workspaces': workspaces})

    # Update Document
    @http.route(['/my/documents/update'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST'])
    def update_document(self, **post):
        redirect_link = '/my/documents/'
        if post.get('document_id') and post.get('document_name'):
            document = request.env[
                'documents.document'].sudo().browse(
                int(post.get('document_id')))
            document.write({
                'name': post.get('document_name')
            })
            redirect_link += str(document.id)
            if post.get('doc_uploaded'):
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
                document.attachment_id = attachment.id
                document.name = post.get('document_name')
            partners = request.env.ref(
                'taxsurety.group_taxsurety_tax_administrators').sudo().users.partner_id.ids
            document.message_subscribe(
                partner_ids=partners)
            body = _('%s updated the document.', request.env.user.name)
            document.message_post(body=body, message_type='email',
                                  partner_ids=document.message_follower_ids.partner_id.ids)
        return request.redirect(redirect_link)

    # Chatter attachment updates

    @http.route()
    def attachment_add(self, name, file, res_model, res_id, access_token=None,
                       **kwargs):
        """
        Overridden to pass document access from JS
        """
        try:
            self._document_check_access(res_model, int(res_id),
                                        access_token=access_token,
                                        document_access=kwargs.get(
                                            'document_access'))
        except (AccessError, MissingError) as e:
            raise UserError(
                _("The document does not exist or "
                  "you do not have the rights to access it."))

        IrAttachment = request.env['ir.attachment']
        access_token = False

        # Avoid using sudo or creating access_token when not necessary: internal
        # users can create attachments, as opposed to public and portal users.
        if not request.env.user._is_internal():
            IrAttachment = IrAttachment.sudo().with_context(
                binary_field_real_user=IrAttachment.env.user)
            access_token = IrAttachment._generate_access_token()

        # At this point the related message does not exist yet, so we assign
        # those specific res_model and res_is. They will be correctly set
        # when the message is created: see `portal_chatter_post`,
        # or garbage collected otherwise: see  `_garbage_collect_attachments`.
        attachment = IrAttachment.create({
            'name': name,
            'datas': base64.b64encode(file.read()),
            'res_model': 'mail.compose.message',
            'res_id': 0,
            'access_token': access_token,
        })
        return request.make_response(
            data=json.dumps(attachment.read(
                ['id', 'name', 'mimetype', 'file_size', 'access_token'])[0]),
            headers=[('Content-Type', 'application/json')]
        )

    def _document_check_access(self, model_name, document_id,
                               access_token=None, document_access=None):
        """Check if current user is allowed to access the specified record.
        The user should be able to add attachments to the chatter.
        """
        document = request.env[model_name].browse([document_id])
        document_sudo = document.with_user(SUPERUSER_ID).exists()
        if not document_sudo:
            raise MissingError(_("This document does not exist."))
        try:
            if not document_access:
                document.check_access_rights('read')
                document.check_access_rule('read')
        except AccessError:
            if not access_token or not document_sudo.access_token or not consteq(
                    document_sudo.access_token, access_token):
                raise
        return document_sudo
