# -*- coding: utf-8 -*-
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.partner'

    header_image = fields.Binary(string="Header Image", attachment=True)
    hero_image_1 = fields.Binary(string="Hero Image 1", attachment=True)
    hero_image_2 = fields.Binary(string="Hero Image 2", attachment=True)
    hero_image_3 = fields.Binary(string="Hero Image 3", attachment=True)
    vision_board_image_gallery_image_1 = fields.Binary(
        string="Vision Board Gallery Image 1", attachment=True)
    vision_board_image_gallery_image_2 = fields.Binary(
        string="Vision Board Gallery Image 2", attachment=True)
