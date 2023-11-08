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
