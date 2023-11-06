odoo.define('taxsurety.composer', function (require) {
'use strict';
//Add Document Access True to Portal Composer
    var PortalComposer = require('portal.composer');

    PortalComposer.PortalComposer.include({
        _prepareAttachmentData: function (file) {
            return {
                'name': file.name,
                'file': file,
                'res_id': this.options.res_id,
                'res_model': this.options.res_model,
                'access_token': this.options.token,
                'document_access': this.options.document_access
            };
        },
    })
})
