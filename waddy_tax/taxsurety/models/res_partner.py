# -*- coding: utf-8 -*-
from odoo import fields, models, _, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_update_contacts_through_excel(self):
        return {
            'name': _("Import Contact"),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'partner.matching.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
