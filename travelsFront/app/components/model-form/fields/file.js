import Ember from 'ember';
import BaseField from './input';

const {
  on,
  get, set,
  computed,
  computed: { alias },
  observer,
  $
} = Ember;


export default BaseField.extend({
  tagName: 'md-content',
  classNames: ['flex-100', 'layout-gt-xs-row', 'file-input'],
  classNamesBindings: alias('fattrs.class'),
  type: 'file',

  fileInputValue: null,
  fileValue: null,
  shouldDelete: false,

  handleFileValueChange: observer('fileValue', function() {
    let value = get(this, 'fileValue');
    if (value) {
      this.sendAction('onChange', value);
    }
  }),

  setInitialURL: on('init', function() {
    set(this, 'initialVal', get(this, 'value'));
    this.updateURL(); 
  }),

  updateURL() {
    let value = get(this, 'value');
    if (typeof value === 'string' || value === null) {
      if (!get(this, 'shouldDelete')) {
        set(this, 'fileURL', value || null);
        if (value) {
          this.setFileInputValue(value);
        } else {
          set(this, 'fileInputValue', null);
        }
      }
    }
  },

  observeValue: observer('value', function() {
    let value = get(this, 'value');
    if (value === null) {
      // this is a server side null
      set(this, 'shouldDelete', false);
      set(this, 'fileValue', null);
      this.updateURL();
    } else if (typeof value === 'string') {
      set(this, 'fileValue', null);
      if (value != '') {
        // a url is set as value
        set(this, 'shouldDelete', false);
        set(this, 'initialVal', value);
        this.updateURL();
      }
    }
  }),

  inputAttrs: {
    readonly: true
  },

  setFileInputValue(val) {
    let parts = val.split("/");
    set(this, 'fileInputValue', parts.pop());
  },

  observeShouldDelete: observer('shouldDelete', function() {
    let del = get(this, 'shouldDelete');
    let inputVal = get(this, 'fileValue');
    let initial = get(this, 'initialVal');

    if (del) {
      // '' is the local null, this is to identify server-side null values 
      // and clear the input field
      this.sendAction('onChange', '');
      this.setFileInputValue(initial);
    } else {
      if (!inputVal && initial) {
        this.sendAction('onChange', initial);
      } else {
        this.sendAction('onChange', inputVal);
      }
    }
  }),
  
  prepareFileEvents: on('didInsertElement', function() {
    this.fileInput = this.$('input.file-input[type=file]');
    this.textInput = this.$('input[type=text]');
    this.textInput.on('click', () => {
      this.actions.handleClick.bind(this)();
    });
    this.fileInput.on('change', () => {
      set(this, 'fileInputValue', this.fileInput.val());
      set(this, 'fileValue', this.fileInput[0].files[0]);
      set(this, 'shouldDelete', false);
    });
  }),

  removeFileEvents: on('willDestroyElement', function() {
    this.fileInput.off('change');
    this.textInput.off('click');
  }),

  fileName: computed('fileURL', function() {
    let url = get(this, 'fileURL');
    if (!url) { return ''; }
    let parts = url.split("/");
    return parts.pop();
  }),

  actions: {
    handleClick() {
      this.fileInput.click();
    },

    toggleShouldDelete() {
      this.toggleProperty('shouldDelete');
    }
  }
});
