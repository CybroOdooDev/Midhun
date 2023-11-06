odoo.define('taxsurety.document_create_portal', function(require) {
'use strict';
    var publicWidget = require('web.public.widget');

    publicWidget.registry.documentCreatePortal = publicWidget.Widget.extend({
        selector: '.folder--create-document',
        events: {
            'click .click_to_upload_doc': '_onUploadDocumentFile',
            },
        _onUploadDocumentFile: function (event) {
            var heading = this.$el.find('div.modal-header h5')
            heading.text('Upload Document for ' + event.currentTarget.getAttribute('data-folder-name'));
        },
    })
})
