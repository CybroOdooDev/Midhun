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

{
    'name': "Taxsurety",
    'version': '16.0.1.1.4',
    'category': 'Accounting',
    'summary': """Taxsurety custom module.""",
    'description': """Taxsurety custom module.""",
    'depends': ['account_accountant',
                'contacts', 'portal',
                'documents', 'website', 'mail',
                'website_sale'],
    'data': [
        'security/group_taxsurety.xml',
        'security/ir.model.access.csv',
        'data/document_mail_template.xml',
        'data/server_action.xml',
        'views/documents_folder_views.xml',
        'views/portal_views.xml',
        'views/document_details.xml',
        'views/portal_layout.xml',
        'views/templates.xml',
        'views/website_views.xml',
        'views/portal_updates.xml',
        'views/res_partner_views.xml',
        'views/account_portal_templates.xml',
        'wizards/import_excel_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'taxsurety/static/src/css/taxsurety.css',
            'taxsurety/static/src/js/portal_composer.js',
            'taxsurety/static/src/js/portal_updates.js',
            'taxsurety/static/src/js/document_uploader.js',
            'taxsurety/static/src/js/document_create_portal.js',
            'taxsurety/static/src/js/account_portal.js',
        ]
    },
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
