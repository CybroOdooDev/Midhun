# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.home import ensure_db, Home, SIGN_UP_REQUEST_PARAMS, LOGIN_SUCCESSFUL_PARAMS
from odoo.addons.auth_signup.controllers.main import AuthSignupHome


class TaxsuretySignup(AuthSignupHome):
    @http.route()
    def web_auth_signup(self):
        qcontext = {k: v for (k, v) in request.params.items() if
                    k in SIGN_UP_REQUEST_PARAMS}
        qcontext.update(self.get_auth_signup_config())
        if not qcontext.get('token') and request.session.get(
                'auth_signup_token'):
            qcontext['token'] = request.session.get('auth_signup_token')
        if qcontext.get('token'):
            try:
                # retrieve the user info (name, login or email) corresponding to a signup token
                token_infos = request.env[
                    'res.partner'].sudo().signup_retrieve_info(
                    qcontext.get('token'))
                for k, v in token_infos.items():
                    qcontext.setdefault(k, v)
            except:
                qcontext['invalid_token'] = True
                if request.website.is_signup_disabled:
                    return request.redirect('/shop')
        elif not qcontext.get('token'):
            if request.website.is_signup_disabled:
                return request.redirect('/shop')
        return super(TaxsuretySignup, self).web_auth_signup()
