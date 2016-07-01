import Ember from 'ember';
import _ from 'lodash/lodash';

const {
  computed,
  computed: { notEmpty, reads, alias },
  mixin,
  getWithDefault,
  observer,
  get,
  set
} = Ember;


// as seen @ https://github.com/martndemus/ember-form-for/blob/master/addon/utils/strings.js
const {
  String: { capitalize, decamelize }
} = Ember;
const WORD_SEPERATORS = new RegExp('[-_\. ]', 'g');
export const titlecase = (string) =>
  decamelize(string)
    .split(WORD_SEPERATORS)
    .map((w) => capitalize(w))
    .join(' ');


export default Ember.Component.extend({

  tagName: 'md-content',
  classNames: ['layout-column'],

  classNameBindings: ['flexCls'],
  flexCls: computed('flex', 'options.flex', function() {
    if (this.get('flex')) {
      return 'flex-' + this.get('flex');
    }
    return 'flex-100';
  }),

  init() {
    this._super(...arguments);
    this.kwargs = Ember.Object.create();
  },

  store: Ember.inject.service('store'),

  options: alias('field.options'),
  key: reads('field.key'),

  isRelationship: reads('field.isRelationship'),
  isSelect: reads('isRelationship'),

  label: computed('field', 'field.options.label', function() {
    return this.get('field.options.label') || titlecase(this.get('key'));
  }),

  placeholder: computed('fieldComponent', function() {
    if (this.get('isSelect')) {
      return this.get('label');
    }
    return null;
  }),

  fieldComponent: computed('field', function() {
    let field = this.get('field');
    let key = 'paper-input';
    if (field.fieldType) { return field.fieldType; }
    if (this.get("isSelect")) { key = 'paper-select'; }
    if (field.type === 'boolean') { key = 'paper-checkbox'; }
    return key;
  }),

  // select related method
  getOptions: computed('options', 'options.getOptions', function() {
    let getOptions = this.get('options.getOptions');
    if (Ember.isArray(getOptions)) { 
      return function() {
        return new Ember.RSVP.Promise(function() {
          return getOptions;
        });
      };
    }

    if (getOptions) { return getOptions; }
    if (this.get('isRelationship')) {
      let type = this.get('field.type');
      return function() {
        return this.get("store").findAll(type);
      }.bind(this);
    }
  }),

  // select related method
  getOptionLabel: computed('field', function(i) {
    let key = this.get('options.labelKey') || 'name';
    let isRel = this.get('isRelationship');
    return function(item) {
      if (isRel) {
        return item.get(key);
      } else {
        if (_.isString(i)) {
          return i;
        }
        return item.label;
      }
    };
  }),

  propertyDidChange: observer('field', function() {
    let key = this.get('key');

    mixin(this, {
      rawValue: reads(`object.${key}`),
      errors: reads(`object.validations.attrs.${key}.errors`),
      hasErrors: notEmpty(`object.validations.attrs.${key}.errors`),
    });

    let attrs = this.get('field.options.fieldAttrs') || {};
    Ember.keys(attrs).forEach((k) => set(this, k, attrs[k]));

    if (this.get('isRelationship')) {
      mixin(this, {
        rawValueObserver: observer(`object.${key}.id`, function() {
          this.set('rawValue', this.get('object.' + this.get('key')));
        })
      });
    }

    if (this.get('isSelect')) {
      mixin(this, {
        getItems: reads(`getOptions`),
        itemLabelCallback: reads(`getOptionLabel`)
      });
    }
  }),

  value: computed('rawValue', function() {
    let serializeValue = getWithDefault(this, 'serializeValue', (value) => value);
    let raw = get(this, 'rawValue');
    if (raw instanceof Ember.ObjectProxy) {
      raw.then(function(v) {
        this.set('rawValue', v);
      }.bind(this));
      return null;
    }
    let v = serializeValue(raw);
    return v;
  }),

  didReceiveAttrs() {
    this._super(...arguments);
    this.propertyDidChange();
  },
  
  actions: {
    updateProperty: function(value) {
      set(this.get('object'), this.get('key'), value);
    }
  }
});
