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

from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale


class TaxsuretyShop(WebsiteSale):
    @route()
    def shop(self, page=0, category=None, search='', min_price=0.0,
             max_price=0.0, ppg=False, **post):
        if request.website.is_shop_disabled:
            return request.redirect('/')
        else:
            return super().shop(page=page, category=category,
                                search=search, ppg=ppg, min_price=min_price,
                                max_price=max_price, **post)

    @route()
    def shop_payment(self, **post):
        if request.website.is_shop_disabled:
            return request.redirect('/')
        else:
            return super().shop_payment(**post)

    @route()
    def checkout(self, **post):
        if request.website.is_shop_disabled:
            return request.redirect('/')
        else:
            return super().checkout(**post)

    @route()
    def shop_payment_confirmation(self, **post):
        if request.website.is_shop_disabled:
            return request.redirect('/')
        else:
            return super().shop_payment_confirmation(**post)

