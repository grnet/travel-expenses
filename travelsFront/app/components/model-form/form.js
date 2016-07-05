import Ember from 'ember';
import _ from 'lodash/lodash';

var getKeys = Object.keys;
var get = Ember.get;
var set = Ember.set;
var TypesCache = {};

const ModelForm = Ember.Component.extend({

  tagName: 'form',
  isTouched: false,
  classNames: ['model-form'],
  validationErrors: Ember.computed.alias('model.validations.errors'),
  validation: Ember.computed.alias('model.validations.attrs'),
  isValid: Ember.computed.alias('model.validations.isValid'),
  modelErrors: Ember.computed.alias('model.errors'),

  didReceiveAttrs() {
    this._super(...arguments);
    let model = this.get("model");
    let type = model.constructor;
    let meta = this.extractMetaForType(type);
    this.setProperties({model, type, meta});
  },

  handleErrors: Ember.observer('validationErrors.@each', function() {
    this.updateValidationErrors(this.get('model'));
  }),

  fieldsets: null,

  extractMetaForType(type) {
    if (TypesCache[type]) { return TypesCache[type]; }
    let formParams = type.prototype.__form__ || {};
    let layout = this.get("flexLayout") || formParams.layout || "100";
    if (!Ember.isArray(layout)) { layout = layout.split(" "); }

    let meta = {fields: {}, keys: [], fieldsList: []};
    let fields = get(type, 'fields');
    let unordered = {};
    type.eachAttribute((k,v) => { unordered[k] = v; v.key = v.name; });
    type.eachRelationship((k,v) => { unordered[k] = v; });
    let keys = fields._keys.list;
    meta.keys = keys;

    let defaultFlex = layout[layout.length - 1];
    meta.keys.forEach((key, i) => {
      let field = unordered[key];
      field.layout = {flex: layout[i] || defaultFlex};
      meta.fields[key] = field;
      meta.fieldsList.push(field);
    });
    formParams.fieldsets = formParams.fieldsets || undefined;
    let fieldsets = [];
    if (formParams.fieldsets) {
      formParams.fieldsets.forEach(function(f) {
        fieldsets.push({
          fields: f.fields.map((k) => meta.fields[k]),
          label: f.label,
          flexLayout: '100' 
        })
      });
      meta.fieldsets = fieldsets;
    };
    return meta;
  },

  clearModelErrors: function(errors) {
    if (!errors) { return; }
    // TODO: skip clearing of unmodified server side errors, somehow
    getKeys(errors).forEach(function(k) {
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
      this.actions.submit.call(this);
    }
  },

  actions: {
    submit() {
      let model = this.get("model");
      let isValid = get(this, "isValid");
      this.setProperties({'formSuccess': null, 'formError': null});
      set(this, 'isTouched', true);
      if (isValid) {
        model.save().then(() => {
          this.set('formSuccess', 'Success');
        }).catch((err) => {
          this.set('formError', err.message);
        });
        return true;
      } else {
        this.updateValidationErrors(model);
        return false;
      }
    },

    reset() {
      // TODO: how to rollback relationships???
      this.get("model").rollbackAttributes();
    }
  }
});

ModelForm.reopenClass({
  positionalParams: ['model'],
});

export default ModelForm;
