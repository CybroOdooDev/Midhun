odoo.define('taxsurety.portal_updates', function(require) {
'use strict';
    var publicWidget = require('web.public.widget');
    publicWidget.registry.portalUpdates = publicWidget.Widget.extend({
        selector: '.o_portal_my_home',
        events: {
            'click a[data-bs-target="#UpdateContactFolders"]': '_onUpdateContactFolders',
            },
        _onUpdateContactFolders: function (event) {
            this.$el.find(
            '#UpdateContactFolders h5.se-modal__title').text(
            'Update your ' + event.currentTarget.getAttribute('data-h5') + ' Tax Payment');
            this.$el.find('#UpdateContactFolders input#field_name').val(
            event.currentTarget.getAttribute('data-h5'));
        },
    });
});
