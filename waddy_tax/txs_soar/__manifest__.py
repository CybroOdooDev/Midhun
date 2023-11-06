# -*- coding: utf-8 -*-
{
    'name': "TxsSoar",
    'version': '16.0.1.0.0',
    'category': 'Others',
    'summary': """TxsSoar custom module.""",
    'description': """TxsSoar custom module.""",
    'depends': ['base', 'web', 'website'],
    'data': [
        'data/data.xml',
        'views/res_users_views.xml',
        'views/snippets/s_picture_txs_soar.xml',
        'views/snippets/s_rss_feed.xml',
        'views/snippets/snippets.xml',
        'views/res_config_settings_views.xml',
        'views/portal.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'txs_soar/static/src/js/s_rss_feed.js',
            'txs_soar/static/src/css/s_rss_feed.css',
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
