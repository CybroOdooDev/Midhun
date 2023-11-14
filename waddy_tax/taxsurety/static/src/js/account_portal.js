odoo.define('taxsurety.account_portal', function(require) {
'use strict';
    var publicWidget = require('web.public.widget');
    publicWidget.registry.AccountPortalTaxsurety = publicWidget.Widget.extend({
        selector: '.o_portal_invoice_sidebar',
        events: {
            'click #downpayment_check': '_onClickDownpayment',
            'click .pay-now-button a': '_onClickPayNow',
            },
        _onClickDownpayment: function (event) {
            if (this.$el.find('#downpayment_check').is(':checked')) {
                    this.$el.find('.price_display').removeClass('d-none');
                }
            else{
                this.$el.find('.price_display').addClass('d-none');
            }
        },
        _onClickPayNow: function (event) {
            console.log(this.$el.find('form.o_payment_checkout').attr('data-amount', 24.0))
        }
    })
})