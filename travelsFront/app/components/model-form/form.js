import FlexMixin from 'ember-paper/mixins/flex-mixin';
import Ember from 'ember';
import _ from 'lodash/lodash';
import {ResourceMetaFrom} from './util';

const {
  get, set, computed: { alias }
} = Ember
var TypesCache = {};

const ModelForm = Ember.Component.extend(FlexMixin, {
  
  tagName: 'form',
  isTouched: false,
  classNames: ['model-form'],
  validationErrors: Ember.computed.alias('model.validations.errors'),
  validation: Ember.computed.alias('model.validations.attrs'),
  isValid: Ember.computed.alias('model.validations.isValid'),
  modelErrors: Ember.computed.alias('model.errors'),
  submitLabel: 'Save',

  didReceiveAttrs() {
    this._super(...arguments);
    let object = this.get("model");
    let ui = this.get("ui") || "default";
    let meta = ResourceMetaFrom(object, null, ui);
    window['meta'] = meta;
    this.setProperties({object, meta});
    let parent = this.get('registerForm');
    if (parent){
      set(parent, 'modelform', this);
    } 
  },

  handleErrors: Ember.observer('validationErrors.@each', function() {
    this.updateValidationErrors(this.get('model'));
  }),

  fieldsets: alias('meta.fieldsets'),

  clearModelErrors: function(errors) {
    if (!errors) { return; }
    // TODO: skip clearing of unmodified server side errors, somehow
    Object.keys(errors).forEach(function(k) {
      errors.set(k, null);
    });
  },

  updateValidationErrors: function() {
    let validationErrors = get(this, 'validationErrors');
    let modelErrors = get(this, 'modelErrors');

    let errors = _.groupBy(validationErrors, (e) => e.get('attribute'));
    this.clearModelErrors(modelErrors);
    modelErrors.setProperties(errors);
  },

  keyPress: function(e) {
    if (e.which === 13) {
      if (e.target && e.target.tagName.toLowerCase() !== "textarea") {
        let submit = this.get('submit');
        if (submit) { return submit(this); }
        return this.actions.submit.call(this);
      }
    }
  },

  isInvalid: false,
  submitFailed: false,

  resetMessages: function() {
    this.setProperties({
      'submitMessage': '', 
      'submitError': '',
      'isInvalid': false,
      'submitFailed': false
    });
  },

  getModelForSave() {
    return this.get('model');
  },

  actions: {
    submit(event, ...args) {
      if (this.get("submit")) { return this.get("submit")(this); }
      //let model = this.get("model");
      let model = this.getModelForSave(...args);
      let isValid = get(this, "isValid");
      this.resetMessages();
      set(this, 'isTouched', true);
      if (isValid) {
        this.set('inProgress', true);
        model.save().then(() => {
          this.set('submitMessage', 'Form saved');
          this.sendAction('onSuccess', model);
        }).catch((err) => {
          let errMessage = err.message;
          this.sendAction('onError', model);
          if (err.isAdapterError) {
            errMessage = "Form submission failed";
            if (err.errors && err.errors.length && err.errors[0].detail) {
              errMessage = errMessage + " (" + err.errors[0].detail + ")";
            }
          }
          this.set('submitError', errMessage);
          this.set('submitFailed', true);
          console.error("model.errors")
          console.error(err);
        }).finally(() => { this.set('inProgress', false)});
        return true;
      } else {
        this.updateValidationErrors(model);
        this.set("isInvalid", true);
        console.error(model.get('errors'));
        return false;
      }
    },

    reset() {
      if (this.get("submit")) { return this.get("submit")(this); }
      // TODO: how to rollback relationships???
      this.resetMessages();
      if (this.get("model.id")) {
        this.get("model").rollbackAttributes();
      }
    }
  }
});

ModelForm.reopenClass({
  positionalParams: ['model'],
});

export default ModelForm;
