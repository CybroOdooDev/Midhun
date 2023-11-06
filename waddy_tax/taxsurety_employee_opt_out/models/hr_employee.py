# -*- coding: utf-8 -*-
from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_opt_out = fields.Boolean(string='Opt out from reminder',
                                default=False,
                                help="Enable this checkbox to "
                                     "opt out the employee from receiving "
                                     "timesheet reminder.")
