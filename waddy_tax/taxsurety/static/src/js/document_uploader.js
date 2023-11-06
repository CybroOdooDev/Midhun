odoo.define('taxsurety.document_uploader', function(require) {
'use strict';
    var publicWidget = require('web.public.widget');

    publicWidget.registry.documentUploader = publicWidget.Widget.extend({
        selector: '#wrapwrap',
        events: {
            'click .upload-doc': '_onUploadDoc',
            'change #doc_uploader_document_upload': '_onFileChange',
            'change #doc_uploader_folder_upload': '_onFileChangeFolder',
            'change #doc_uploader_details': '_onFileChangeDetails',
            'click .click_to_upload_doc': '_onUploadDocumentFile',
            'submit .submission__form': '_onSubmitLoader',
            },

        _onUploadDoc: function (event) {
            var heading = this.$el.find('div.modal-header h5')
            heading.text('Upload Document for ' + event.currentTarget.getAttribute('data-document-name'))
            var sub = this.$el.find('div#click-image-document')
            sub.text('Click on the image to upload Document for ' + event.currentTarget.getAttribute('data-document-name'))
            var doc_id = this.$el.find('input#document_id')
            doc_id.val(event.currentTarget.getAttribute('data-document-id'))
        },

        _onFileChange: function (event)
        {
            var file = event.target.files
            if (file.length == 0) {
                $('#loader__container').show()
            }
            else{
                $('#loader__container').hide()
                if (file[0]) {
                    if(file[0].type.includes("video")) {
                        this.$el.find('#label_for_doc_uploader_document_upload').empty();
                        this.$el.find('#label_for_doc_uploader_document_upload').append(
                        '<video id="doc_uploaded_document_upload" style="cursor:pointer; width: 60%; height: 90%"/>');
                        this.el.querySelector('#doc_uploaded_document_upload').src = URL.createObjectURL(file[0]);
                        this.el.querySelector('#file_name_document_upload').value = file[0].name;
                        this.el.querySelector('#file_type_document_upload').value = file[0].type;
                    }
                    else if(file[0].type.includes("image")) {
                        this.$el.find('#label_for_doc_uploader_document_upload').empty();
                        this.$el.find('#label_for_doc_uploader_document_upload').append(
                        '<img id="doc_uploaded_document_upload" style="cursor:pointer; width: 60%; height: 90%"/>');
                        this.el.querySelector('#doc_uploaded_document_upload').src = URL.createObjectURL(file[0]);
                        this.el.querySelector('#file_name_document_upload').value = file[0].name;
                        this.el.querySelector('#file_type_document_upload').value = file[0].type;
                    }
                    else if(file[0].type.includes("application/pdf")) {
                        this.$el.find('#label_for_doc_uploader_document_upload').empty();
                        this.$el.find('#label_for_doc_uploader_document_upload').append(
                        '<iframe id="doc_uploaded_document_upload" style="cursor:pointer; width: 60%; height: 90%"/>');
                        this.el.querySelector('#doc_uploaded_document_upload').src = URL.createObjectURL(file[0]);
                        this.el.querySelector('#file_name_document_upload').value = file[0].name;
                        this.el.querySelector('#file_type_document_upload').value = file[0].type;
                    }
                    else if(file[0].type.includes("application/vnd")) {
                        if(file[0].type.includes("ms-excel") || file[0].type.includes("spreadsheetml.sheet")) {
                            this.$el.find('#label_for_doc_uploader_document_upload').empty();
                            this.$el.find('#label_for_doc_uploader_document_upload').append(
                            '<img id="doc_uploaded_document_upload" src="/taxsurety/static/src/images/excel.svg" style="cursor:pointer; height: 150px;"/>');
                        }
                    }
                    else {
                        this.$el.find('#label_for_doc_uploader_document_upload').empty();
                        this.$el.find('#label_for_doc_uploader_document_upload').html(
                        'Unsupported file. Cannot show Preview. <i class="fa fa-upload" style="cursor: pointer; margin-left: 10px;" title="Re-upload"/>');
                    }
                }
            }
        },

        _onFileChangeFolder: function (event)
        {
            var file = event.target.files
            if (file[0]) {
                if(file[0].type.includes("video")) {
                    this.$el.find('#label_for_doc_uploader_folder_upload').empty();
                    this.$el.find('#label_for_doc_uploader_folder_upload').append(
                    '<video id="doc_uploaded_folder_upload" style="cursor:pointer; width: 60%; height: 90%"/>');
                    this.el.querySelector('#doc_uploaded_folder_upload').src = URL.createObjectURL(file[0]);
                    this.el.querySelector('#file_name_folder_upload').value = file[0].name;
                    this.el.querySelector('#file_type_folder_upload').value = file[0].type;
                }
                else if(file[0].type.includes("image")) {
                    this.$el.find('#label_for_doc_uploader_folder_upload').empty();
                    this.$el.find('#label_for_doc_uploader_folder_upload').append(
                    '<img id="doc_uploaded_folder_upload" style="cursor:pointer; width: 60%; height: 90%"/>');
                    this.el.querySelector('#doc_uploaded_folder_upload').src = URL.createObjectURL(file[0]);
                    this.el.querySelector('#file_name_folder_upload').value = file[0].name;
                    this.el.querySelector('#file_type_folder_upload').value = file[0].type;
                }
                else if(file[0].type.includes("application/pdf")) {
                    this.$el.find('#label_for_doc_uploader_folder_upload').empty();
                    this.$el.find('#label_for_doc_uploader_folder_upload').append(
                    '<iframe id="doc_uploaded_folder_upload" style="cursor:pointer; width: 60%; height: 90%"/>');
                    this.el.querySelector('#doc_uploaded_folder_upload').src = URL.createObjectURL(file[0]);
                    this.el.querySelector('#file_name_folder_upload').value = file[0].name;
                    this.el.querySelector('#file_type_folder_upload').value = file[0].type;
                }
                else if(file[0].type.includes("application/vnd")) {
                    if(file[0].type.includes("ms-excel") || file[0].type.includes("spreadsheetml.sheet")) {
                        this.$el.find('#label_for_doc_uploader_folder_upload').empty();
                        this.$el.find('#label_for_doc_uploader_folder_upload').append(
                        '<img id="doc_uploaded" src="/taxsurety/static/src/images/excel.svg" style="cursor:pointer; height: 150px;"/>');
                    }
                }
                else {
                    this.$el.find('#label_for_doc_uploader_folder_upload').empty();
                    this.$el.find('#label_for_doc_uploader_folder_upload').html(
                    'Unsupported file. Cannot show Preview. <i class="fa fa-upload" style="cursor: pointer; margin-left: 10px;" title="Re-upload"/>');
                }
            }
        },

        _onUploadDocumentFile: function (event) {
            var heading = this.$el.find('#UploadDocumentFolder h5')
            var sub = this.$el.find('div#click-image-document_folder')
            heading.text('Upload Document to folder ' + event.currentTarget.getAttribute('data-folder-name'));
            sub.text('Click on the image to upload Document to folder ' + event.currentTarget.getAttribute('data-folder-name'));
            var doc_id = this.$el.find('input#folder_document_id')
            doc_id.val(event.currentTarget.getAttribute('data-folder-id'))
        },

        _onFileChangeDetails: function (event)
        {
            var labelReUploadButton = $('label[for="'+ event.target.id + '"]').find('#reUploadButton')
            if (labelReUploadButton) {
                var file = event.target.files
                if (file[0]) {
                    if(file[0].type.includes("image")) {
                        this.$el.find('.col--preview-container').empty();
                        this.$el.find('.col--preview-container').append(
                        `<img class="doc_image"/>
                        <label for="doc_uploader_details"
                         class="mt-2"
                         id="label_for_doc_uploader_document_upload"
                               style="display: flex; justify-content: center; width: inherit;">
                            <div id="reUploadButton"
                                    class="reupload_button btn btn-primary">
                            Re-upload
                            </div>
                        </label>`);
                        this.el.querySelector('.col--preview-container img').src = URL.createObjectURL(file[0]);
                        this.el.querySelector('#file_name_document_upload').value = file[0].name;
                        this.el.querySelector('#file_type_document_upload').value = file[0].type;
                    }

                    else if(file[0].type.includes("video")) {
                        this.$el.find('.col--preview-container').empty();
                        this.$el.find('.col--preview-container').append(
                        `<video class="doc_image"/>
                        <label for="doc_uploader_details"
                         class="mt-2"
                         id="label_for_doc_uploader_document_upload"
                               style="display: flex; justify-content: center; width: inherit;">
                            <div id="reUploadButton"
                                    class="reupload_button btn btn-primary">
                            Re-upload
                            </div>
                        </label>`);
                        this.el.querySelector('.col--preview-container video').src = URL.createObjectURL(file[0]);
                        this.el.querySelector('#file_name_document_upload').value = file[0].name;
                        this.el.querySelector('#file_type_document_upload').value = file[0].type;
                    }

                    else if(file[0].type.includes("application/pdf")) {
                        this.$el.find('.col--preview-container').empty();
                        this.$el.find('.col--preview-container').append(
                        `<iframe style="width: 100%; height: 300px; border: 1px solid;"/>
                        <label for="doc_uploader_details"
                         class="mt-2"
                         id="label_for_doc_uploader_document_upload"
                               style="display: flex; justify-content: center; width: inherit;">
                            <div id="reUploadButton"
                                    class="reupload_button btn btn-primary">
                            Re-upload
                            </div>
                        </label>`);
                        this.el.querySelector('.col--preview-container iframe').src = URL.createObjectURL(file[0]);
                        this.el.querySelector('#file_name_document_upload').value = file[0].name;
                        this.el.querySelector('#file_type_document_upload').value = file[0].type;
                    }
                    else if(file[0].type.includes("application/vnd")) {
                        if(file[0].type.includes("ms-excel") || file[0].type.includes("spreadsheetml.sheet")) {
                            this.$el.find('.col--preview-container').empty();
                        this.$el.find('.col--preview-container').append(
                            `<img src="/taxsurety/static/src/images/excel.svg"
                             style="cursor:pointer; height: 150px;"/>
                             <label for="doc_uploader_details"
                             class="mt-2"
                             id="label_for_doc_uploader_document_upload"
                                   style="display: flex; justify-content: center; width: inherit;">
                                <div id="reUploadButton"
                                        class="reupload_button btn btn-primary">
                                Re-upload
                                </div>
                            </label>`);
                        }
                    }
                    else {
                        this.$el.find('.col--preview-container').empty();
                        this.$el.find('.col--preview-container').html(
                        `Unsupported file. Cannot show Preview. <label for="doc_uploader_details"
                             class="mt-2"
                             id="label_for_doc_uploader_document_upload"
                                   style="display: flex; justify-content: center; width: inherit;">
                                <div id="reUploadButton"
                                        class="reupload_button btn btn-primary">
                                Re-upload
                                </div>
                            </label>`);
                    }
                }
            }
            else {
                var file = event.target.files
                if (file[0]) {
                    if(file[0].type.includes("video")) {
                    this.$el.find('#label_for_doc_uploader_document_upload').empty();
                    this.$el.find('#label_for_doc_uploader_document_upload').append(
                    '<video id="doc_uploaded_document_upload" style="cursor:pointer; width: 60%; height: 90%"/>');
                    this.el.querySelector('#doc_uploaded_document_upload').src = URL.createObjectURL(file[0]);
                    this.el.querySelector('#file_name_document_upload').value = file[0].name;
                    this.el.querySelector('#file_type_document_upload').value = file[0].type;
                }
                    else if(file[0].type.includes("image")) {
                    this.$el.find('#label_for_doc_uploader_document_upload').empty();
                    this.$el.find('#label_for_doc_uploader_document_upload').append(
                    '<img id="doc_uploaded_document_upload" style="cursor:pointer; width: 60%; height: 90%"/>');
                    this.el.querySelector('#doc_uploaded_document_upload').src = URL.createObjectURL(file[0]);
                    this.el.querySelector('#file_name_document_upload').value = file[0].name;
                    this.el.querySelector('#file_type_document_upload').value = file[0].type;
                }
                    else if(file[0].type.includes("application/pdf")) {
                    this.$el.find('#label_for_doc_uploader_document_upload').empty();
                    this.$el.find('#label_for_doc_uploader_document_upload').append(
                    '<iframe id="doc_uploaded_document_upload" style="cursor:pointer; width: 60%; height: 90%"/>');
                    this.el.querySelector('#doc_uploaded_document_upload').src = URL.createObjectURL(file[0]);
                    this.el.querySelector('#file_name_document_upload').value = file[0].name;
                    this.el.querySelector('#file_type_document_upload').value = file[0].type;
                }
                    else if(file[0].type.includes("application/vnd")) {
                    if(file[0].type.includes("ms-excel") || file[0].type.includes("spreadsheetml.sheet")) {
                        this.$el.find('#label_for_doc_uploader_document_upload').empty();
                        this.$el.find('#label_for_doc_uploader_document_upload').append(
                        '<img id="doc_uploaded_document_upload" src="/taxsurety/static/src/images/excel.svg" style="cursor:pointer; height: 150px;"/>');
                    }
                }
                    else {
                    this.$el.find('#label_for_doc_uploader_document_upload').empty();
                    this.$el.find('#label_for_doc_uploader_document_upload').html(
                    'Unsupported file. Cannot show Preview. <i class="fa fa-upload" style="cursor: pointer; margin-left: 10px;" title="Re-upload"/>');
                }
                }
            }
        },

        _onSubmitLoader: function () {
            this.$el.find('#loader__container').show();
        },
    })
});
