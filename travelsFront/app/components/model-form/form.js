import FlexMixin from 'ember-paper/mixins/flex-mixin';
import Ember from 'ember';
import _ from 'lodash/lodash';
import {ResourceMetaFrom} from './util';

const {
  get, getWithDefault, set, computed: { alias }
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
  submitLabel: Ember.computed('label', function() {
    return this.get('i18n').t('form.button.save');
  }),

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

  // when POST/PUT requests add new objects to the hasMany array, those models 
  // appear as duplicates once the request response gets extracted, we cleanup 
  // relations to avoid this. TODO: fix this in a proper way
  resetModelRelations(model) {
    model.eachRelationship((k, r) => {
      if (r.kind === 'hasMany') {
        let models = model.get(k);
        let toRemove = models.filter((m) => {
          return !m.get("id") && 
            m.get('currentState.stateName').includes('uncommitted');
        });
        toRemove.forEach(models.removeObject.bind(models));
      }
    });
  },

  resolveFormErrors: function(errors, model) {
    let formErrors = [];
    for (let error of errors) {
      if (error.detail && error.detail.non_field_errors) {
        formErrors = formErrors.concat(error.detail.non_field_errors);
      }
      if (typeof error.detail === "string" && error.source && error.source.pointer == "/data") {
        formErrors.push(error.detail);
      }
    }
    console.log("resolved errors", formErrors);
    return formErrors;
  },

  scrollToMessage: function(err) {
    if (!this.get('noScroll')) {
      let scrollTo = 0;
      if (err) {
        let invalid = this.$(".md-input-invalid");
        if (invalid.length) {
          scrollTo = invalid.offset().top || 0;
        }
      }
      this.$().parent().animate({
        scrollTop: scrollTo
      });
    }
  },

  actions: {

    submit(event, ...args) {
      if (this.get("submit")) { return this.get("submit")(this); }
      //let model = this.get("model");
      let model = this.getModelForSave(...args);
      let _model = model;
      if (!(model instanceof Ember.RSVP.Promise)) {
        model = new Ember.RSVP.Promise((resolve, reject) => {
          resolve(_model);
        });
      }
      return model.then((model) => {
        let isValid = get(this, "isValid");
        this.resetMessages();
        set(this, 'isTouched', true);
        if (isValid) {
          this.updateValidationErrors();
          this.set('inProgress', true);
          model.save().then(() => {
            this.resetModelRelations(model);
            this.set('submitMessage', getWithDefault(this, 'successMessage', 'Form saved'));
            this.sendAction('onSuccess', model);
            this.scrollToMessage();
          }).catch((err) => {
            let errMessage = err.message;
            if (err.isAdapterError) {
              errMessage = "Form submission failed";
              let formErrors = this.resolveFormErrors(err.errors, model);
              if (formErrors.length) {
                let msg = formErrors.join("\n");
                errMessage += ` (${msg})`;
              }
            }
            this.set('submitError', errMessage);
            this.set('submitFailed', true);
            this.sendAction('onError', model, err);
            this.scrollToMessage(err);
          }).finally(() => { this.set('inProgress', false)});
          return true;
        } else {
          this.updateValidationErrors(model);
          this.set("isInvalid", true);
          console.error(model.get('errors'));
          return false;
        }
      }).catch(function(err) { console.error(err); });
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
