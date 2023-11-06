# -*- coding: utf-8 -*-
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class TaxsuretyShop(WebsiteSale):
    def shop(self, page=0, category=None, search='', min_price=0.0,
             max_price=0.0, ppg=False, **post):
        if request.website.is_shop_disabled:
            return request.redirect('/')
        else:
            return super().shop(page=page, category=category,
                                search=search, ppg=ppg, min_price=min_price,
                                max_price=max_price, **post)

    def shop_payment(self, **post):
        if request.website.is_shop_disabled:
            return request.redirect('/')
        else:
            return super().shop_payment(**post)

    def checkout(self, **post):
        if request.website.is_shop_disabled:
            return request.redirect('/')
        else:
            return super().checkout(**post)

    def shop_payment_confirmation(self, **post):
        if request.website.is_shop_disabled:
            return request.redirect('/')
        else:
            return super().shop_payment_confirmation(**post)

