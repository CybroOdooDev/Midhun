# -*- coding: utf-8 -*-
from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    is_shop_disabled = fields.Boolean(string="Disable Shop",
                                      default=False,
                                      help="Enabling this will remove shop.")
    is_signup_disabled = fields.Boolean(string="Redirect to shop on"
                                               " Signup",
                                        help="Enabling this will"
                                             " redirect to shop "
                                             "page when you click "
                                             "on 'Don't have an account.'",
                                        default=False)
