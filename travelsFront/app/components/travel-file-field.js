import Ember from 'ember';
import BaseFieldMixin from 'ember-gen/lib/base-field';
import ENV from '../config/environment';
import { uploadFile } from '../utils/files';

const {
  get, set,
  computed,
  computed: { reads },
  inject,
} = Ember;

export default Ember.Component.extend(BaseFieldMixin, {

  tagName: 'div',
  multiple: reads('fattrs.multiple'),
  replace: reads('fattrs.replace'),
  img: reads('fattrs.img'),
  readonly: reads('field.readonly'),
  disabled: reads('field.disabled'),
  preventDelete: reads('fattrs.preventDelete'),
  session: inject.service('session'),
  messages: inject.service('messages'),
  inProgress: false,
  attributeBindings: ['disabled'],

  inputAttrs: {
    readonly: true,
  },

  file: computed('value', function(){
    return get(this, 'value');
  }),

  fileURL: computed('file', function(){
    let file = get(this, 'file');

    return `${file}`;
  }),

  fileName: computed('fileURL', function(){
    let url = get(this, 'fileURL');

    if (!url) { return ''; }
    let parts = url.split('/');

    return parts.pop();
  }),

  canAdd: computed('file', 'multiple', function() {
    return get(this, 'multiple') ? true : !get(this, 'file');
  }),

  canDelete: computed('readonly', 'disabled', 'preventDelete', function() {
    let { readonly, disabled, preventDelete } = this.getProperties('readonly', 'disabled', 'preventDelete');

    if (preventDelete) { return false; }

    return !(readonly || disabled);
  }),

  canReplace: computed('readonly', 'disabled', 'replace', function() {
    let { readonly, disabled, replace } = this.getProperties('readonly', 'disabled', 'replace');

    return replace && !(readonly || disabled);
  }),

  reloadRecord() {
    let errors = get(this, 'object._content.errors');

    errors && errors.clear();
    let object = get(this, 'object._content') || get(this, 'object');

    return object.reload().then((record) => {
      let key = get(this, 'field.key');
      let value = get(record, key);
      let change = get(this, `object.${key}`);
      let changeset = get(this, 'object');

      set(this, `object.${key}`, get(record, key));

      return record;
    });
  },

  actions: {

    downloadFile(fileURL, event) {
      event.preventDefault();
      let newWindow = window.open('');

      newWindow.location = fileURL;

      return false;
    },

    deleteFile(file) {
      set(this, 'inProgress', true);
      let object = get(this, 'object._content') || get(this, 'object');
      let key = get(this, 'field.key');

      set(object, key, '');
      set(this, 'value', null);

      return object.save().then(() => {
        return this.reloadRecord().then(() => {
          this.get('messages').setSuccess('file.delete.success');
        });
      }).catch((err) => {
        this.get('messages').setError('file.delete.error');
        throw err;
      }).finally(() => {
        set(this, 'inProgress', false);
      });
    },

    handleAddClick() {
      this.$().find('[type=file]').click();
    },

    onUploadSuccess(file) {
      this.reloadRecord().finally(() => {
        set(this, 'inProgress', false);
      });
      this.$().find('[type=file]').val('');
    },

    handleFile(event) {
      let token = get(this, 'session.session.authenticated.auth_token');
      let id = get(this, 'object.id');
      let file_data_key = get(this, 'field.key');
      let path = get(this, 'fattrs.path');
      let adapter = get(this, 'store').adapterFor(path);
      let url = adapter.buildURL(path, id, 'findRecord');
      let messages = get(this, 'messages');

      let target = event.target || this.fileInput;
      let files = target.files;

      if (!files.length) { return; }

      set(this, 'inProgress', true);
      let file = files[0];

      return uploadFile(file, url, token, file_data_key).then((file) => {
        this.send('onUploadSuccess', file);
        messages.setSuccess('file.upload.success');

        return file;
      }).catch((err) => {
        messages.setError('file.upload.error');
        throw err;
      }).finally((err) => {
        target.value = '';
        set(this, 'inProgress', false);
      });
    },
  },
});
