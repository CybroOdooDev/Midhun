# -*- coding: utf-8 -*-
{
    'name': "Taxsurety Website Appointments",
    'version': '16.0.1.0.0',
    'category': 'Website',
    'summary': """Taxsurety website appointments.""",
    'description': """Taxsurety website appointments.""",
    'depends': ['website', 'calendar', 'appointment'],
    'data': [
        'security/taxsurety_website_appointments_security.xml',
        'views/appointment_type_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
