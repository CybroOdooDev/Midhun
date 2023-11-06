from odoo import http
from odoo.http import request


class TaxSuretyMain(http.Controller):

    @http.route(['/portal'], type='http', auth="user", website=True)
    def portal_taxsurety(self):
        print('hai')
        return request.render("txs_soar.portal_template")
