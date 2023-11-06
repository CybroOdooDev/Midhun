# -*- coding: utf-8 -*-
{
    'name': "Taxsurety Website Snippets",
    'version': '16.0.1.0.0',
    'category': 'Website',
    'summary': """Taxsurety Website Snippets""",
    'description': """Taxsurety Website Snippets""",
    'depends': ['website'],
    'data': [
        'views/taxsurety_website_snippet.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'taxsurety_website_snippet/static/src/js/taxsurety_website_snippet.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
