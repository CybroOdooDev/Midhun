# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request


class PortalUpdates(http.Controller):
    @http.route(['/my/contacts/update'], type='http',
                auth="user", website=True, csrf=False)
    def contacts_update(self, **post):
        if post.get('field_name') and post.get('description'):
            body = _('Update for ' + post.get(
                'field_name') + ': ' + post.get(
                'description'))
            request.env.user.partner_id.message_post(body=body)
        return request.redirect('/my/home')
