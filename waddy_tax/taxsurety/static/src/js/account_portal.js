odoo.define('taxsurety.account_portal', function(require) {
'use strict';
    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');

    publicWidget.registry.AccountPortalTaxsurety = publicWidget.Widget.extend({
        selector: '.o_portal_invoice_sidebar',
        events: {
            'click #downpayment_check': '_onClickDownpayment',
//            'click .pay-now-button': '_onClickPayNow',
            },
        init() {
            this._super.apply(this, arguments);
            console.log('account')
        },


        _onClickDownpayment: function (event) {
            if (this.$el.find('#downpayment_check').is(':checked')) {
                    this.$el.find('.price_display').removeClass('d-none');
                }
            else{
                this.$el.find('.price_display').addClass('d-none');
            }
        },


//        _onClickPayNow: function (event) {
//            var down_payment_check = this.$el.find('#downpayment_check').prop('checked');
//            console.log(down_payment_check)
//            var down_payment_amount = parseFloat(this.$el.find('#price_display_input').val());
//            $.ajax({
//                url:  this.$el.find('form').attr('data-landing-route'),
//                data: ({'down_payment_check': down_payment_check, 'down_payment_amount': down_payment_amount}),
//                type: 'POST',
//            })
//
//        },
    })
})
