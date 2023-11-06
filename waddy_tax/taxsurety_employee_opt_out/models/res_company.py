# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta, time
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class Company(models.Model):
    _inherit = 'res.company'

    @api.model
    def _cron_timesheet_reminder_employee(self):
        """
        Inherit cron to opt out employees from mail
        :return: None
        """
        today_min = fields.Datetime.to_string(datetime.combine(date.today(), time.min))
        today_max = fields.Datetime.to_string(datetime.combine(date.today(), time.max))
        companies = self.search([
            ('timesheet_mail_employee_allow', '=', True),
                '|',
                    '&',
                        ('timesheet_mail_employee_nextdate', '<', today_max), ('timesheet_mail_employee_nextdate', '>=', today_min),
                        ('timesheet_mail_employee_nextdate', '<', today_min)
        ])
        for company in companies:
            if company.timesheet_mail_employee_nextdate < fields.Datetime.today():
                _logger.warning('The cron "Timesheet: Employees Email Reminder" should have run on %s' % company.timesheet_mail_employee_nextdate)

            # get the employee that have at least a timesheet for the last 3 months
            users = self.env['account.analytic.line'].search([
                ('date', '>=', fields.Date.to_string(date.today() - relativedelta(months=3))),
                ('date', '<=', fields.Date.today()),
                ('is_timesheet', '=', True),
                ('company_id', '=', company.id),
            ]).mapped('user_id')

            # calculate the period
            if company.timesheet_mail_employee_interval == 'months':
                date_start = (date.today() - timedelta(days=company.timesheet_mail_employee_delay)) + relativedelta(day=1)
                date_stop = date_start + relativedelta(months=1, days=-1)
            else:
                date_start = date.today() - timedelta(weeks=1, days=company.timesheet_mail_employee_delay - 1)
                date_stop = date_start + timedelta(days=6)

            date_start = fields.Date.to_string(date_start)
            date_stop = fields.Date.to_string(date_stop)

            # get the related employees timesheet status for the cron period
            employees = self.env['hr.employee'].search([('user_id', 'in', users.ids),
                                                        ('is_opt_out', '=', False)])

            work_hours_struct = employees.get_timesheet_and_working_hours(date_start, date_stop)

            for employee in employees:
                if employee.user_id and work_hours_struct[employee.id]['timesheet_hours'] < work_hours_struct[employee.id]['working_hours']:
                    self._cron_timesheet_send_reminder(
                        employee,
                        'timesheet_grid.mail_template_timesheet_reminder_user',
                        'hr_timesheet.act_hr_timesheet_line',
                        additionnal_values=work_hours_struct[employee.id],
                    )

            # compute the next execution date
            companies._calculate_timesheet_mail_employee_nextdate()
