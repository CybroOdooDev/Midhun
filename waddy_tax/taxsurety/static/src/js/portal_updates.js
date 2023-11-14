odoo.define('taxsurety.portal_updates', function(require) {
'use strict';
    var publicWidget = require('web.public.widget');
    publicWidget.registry.portalUpdates = publicWidget.Widget.extend({
        selector: '#wrap',
        events: {
            'click a[data-bs-target="#UpdateContactFolders"]': '_onUpdateContactFolders',
            'click a[data-bs-target="#UpdateOthers"]': '_onUpdateOthers',
            'click a[data-bs-target="#UpdateExpiration"]': '_onUpdateExpiration',
            },
        _onUpdateContactFolders: function (event) {
            this.$el.find(
            '#UpdateContactFolders h5.se-modal__title').text(
            'Update your ' + event.currentTarget.getAttribute('data-h5'));
            this.$el.find('#UpdateContactFolders input#field_name').val(
            event.currentTarget.getAttribute('data-h5'));
        },
        _onUpdateOthers: function (event) {
            this.$el.find('#UpdateOthers h5.se-modal__title').text(
            $(event.currentTarget).attr('title'))
            this.$el.find('#UpdateOthers input#field_name').val(
            event.currentTarget.getAttribute('data-field_name'));
        },
        _onUpdateExpiration: function (event) {
            this.$el.find('#UpdateExpiration input#cc_month_year').attr(
            'value', this.$el.find(
            '#UpdateExpiration input#year').val() + '-' + this.$el.find(
            '#UpdateExpiration input#month').val())

        },
    });
});
