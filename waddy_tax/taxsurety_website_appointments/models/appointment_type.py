# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AppointmentType(models.Model):
    _inherit = 'appointment.type'

    def company_domain(self):
        return [('id', 'in', self.env.user.company_ids.ids)]

    company_id = fields.Many2one('res.company',
                                 string="Company",
                                 related="website_id.company_id",
                                 store=True,
                                 readonly=False,
                                 domain=company_domain)

    def website_domain(self):
        return [('company_id', 'in', self.env.user.company_ids.ids)]

    website_id = fields.Many2one('website',
                                 string="Website",
                                 domain=website_domain)

    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id:
            domain = [('company_id', '=', self.company_id.id)]
        else:
            domain = [('company_id', 'in', self.env.user.company_ids.ids)]
        return {'domain': {'website_id': domain}}
