# -*- coding: utf-8 -*-

import json

from werkzeug.exceptions import NotFound

from odoo import exceptions
from odoo.http import request, route
from odoo.osv import expression
from werkzeug.exceptions import Forbidden


from odoo.addons.website_appointment.controllers.appointment import WebsiteAppointment


class TaxsuretyWebsiteAppointment(WebsiteAppointment):

    @route()
    def appointment_type_page(self, appointment_type_id, state=False,
                              staff_user_id=False, **kwargs):
        """
        Overriding to reroute when
        the appointment of another webiste is accessed by URL.
        """
        appointment_type = self._fetch_and_check_private_appointment_types(
            kwargs.get('filter_appointment_type_ids'),
            kwargs.get('filter_staff_user_ids'),
            kwargs.get('invite_token'),
            current_appointment_type_id=int(appointment_type_id),
        )

        if not appointment_type:
            raise NotFound()

        elif appointment_type.website_id and appointment_type.website_id != request.website:
            return request.redirect('/appointment', 404)

        page_values = self._prepare_appointment_type_page_values(
            appointment_type, staff_user_id, **kwargs)
        return self._get_appointment_type_page_view(appointment_type,
                                                    page_values, state,
                                                    **kwargs)

    @classmethod
    def _appointments_base_domain(cls, filter_appointment_type_ids,
                                  search=False, invite_token=False):

        """Override _appointments_base_domain()
                method to add the filter of website."""
        current_website = request.website
        domain = [('category', '=', 'website'), '|', ('website_id', '=', current_website.id),
                  ('website_id', '=', False)]
        if filter_appointment_type_ids:
            domain = expression.AND([domain, [('id', 'in', json.loads(filter_appointment_type_ids))]])
        if not invite_token:
            country = cls._get_customer_country()
            if country:
                country_domain = ['|', ('country_ids', '=', False), ('country_ids', 'in', [country.id])]
                domain = expression.AND([domain, country_domain])
        # Add domain related to the search bar
        if search:
            domain = expression.AND([domain, [('name', 'ilike', search)]])
        # Because of sudo search, we need to search only published ones if there is no invite_token
        if request.env.user.share and not invite_token:
            domain = expression.AND([domain, [('is_published', '=', True)]])

        return domain

    @staticmethod
    def _fetch_and_check_private_appointment_types(appointment_type_ids,
                                                   staff_user_ids, invite_token,
                                                   current_appointment_type_id=False,
                                                   domain=False):
        """
        Override _fetch_and_check_private_appointment_types() to
        add website domain, used when searching.
        """

        current_website = request.website
        domain = expression.OR([domain,
                                [('website_id', '=', current_website.id),
                                 ('website_id', '=', False)]])

        appointment_type_ids = json.loads(appointment_type_ids or "[]")
        if not appointment_type_ids and current_appointment_type_id:
            appointment_type_ids = [current_appointment_type_id]
        if not appointment_type_ids and domain:
            appointment_type_ids = request.env[
                'appointment.type'].sudo().search(domain).ids
        elif not appointment_type_ids:
            raise ValueError()

        # Check that the current appointment type is include in the filter
        if current_appointment_type_id and current_appointment_type_id not in appointment_type_ids:
            raise ValueError()

        appointment_types = request.env['appointment.type'].browse(
            appointment_type_ids).exists()
        staff_users = request.env['res.users'].sudo().browse(
            json.loads(staff_user_ids or "[]"))

        if invite_token:
            appt_invite = request.env['appointment.invite'].sudo().search(
                [('access_token', '=', invite_token)])
            if not appt_invite or not appt_invite._check_appointments_params(
                    appointment_types, staff_users):
                raise Forbidden()
            # To bypass the access checks in case we are public user
            appointment_types = appointment_types.sudo()
        elif request.env.user.share:
            # Backward compatibility for old version that had their appointment types "published" by default (aka accessible with read access rights)
            appointment_types = appointment_types.sudo().filtered(
                'is_published') or appointment_types

        try:
            appointment_types.check_access_rights('read')
            appointment_types.check_access_rule('read')
        except exceptions.AccessError:
            raise Forbidden()

        current_appointment_type = request.env[
            'appointment.type'].sudo().browse(
            current_appointment_type_id) if current_appointment_type_id else False
        if current_appointment_type:
            return current_appointment_type
        if domain:
            appointment_types = appointment_types.filtered_domain(domain)
        return appointment_types
