# -*- coding: utf-8 -*-
from odoo import models
import logging
_logger = logging.getLogger(__name__)


class DocumentsFolder(models.Model):
    _name = 'documents.folder'
    _order = 'name'
    _inherit = ['documents.folder', 'mail.thread', 'mail.activity.mixin']
