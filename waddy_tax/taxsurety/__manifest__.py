# -*- coding: utf-8 -*-
{
    'name': "Taxsurety",
    'version': '16.0.1.1.2',
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
        'wizards/import_excel_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'taxsurety/static/src/css/taxsurety.css',
            'taxsurety/static/src/js/portal_composer.js',
            'taxsurety/static/src/js/portal_updates.js',
            'taxsurety/static/src/js/document_uploader.js',
            'taxsurety/static/src/js/document_create_portal.js',
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
