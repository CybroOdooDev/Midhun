# -*- coding: utf-8 -*-
{
    'name': "Taxsurety Employee Opt Out",
    'version': '16.0.1.0.0',
    'category': 'Human Resources',
    'summary': """Taxsurety Employee Opt Out.""",
    'description': """Opt out employees from receiving mails.""",
    'depends': ['hr', 'hr_timesheet', 'timesheet_grid'],
    'data': [
        'views/hr_employee_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
