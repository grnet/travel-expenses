import Ember from 'ember';
import _ from 'lodash/lodash';

const {
  computed,
  computed: { notEmpty, reads, alias, equal, gt, or, bool, not },
  mixin,
  getWithDefault,
  observer,
  get,
  set,
  isArray
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
    if (get(this, 'flex')) {
      return 'flex-' + get(this, 'flex');
    }
    return 'flex-100';
  }),

  init() {
    this._super(...arguments);
    this.kwargs = Ember.Object.create();
  },

  store: Ember.inject.service('store'),

  canShowHint: computed('hint', 'errors', 'errors.[]', function() {
    if (get(this, 'errors.length')) { return false; }
    if (get(this, 'hint')) { return true; }
  }),

  key: reads('field.key'),
  hint: reads('field.hint'),
  isRelation: equal('field.type', 'relation'),
  hasChoices: bool('field.choices'),
  isSelect: or('hasChoices', 'isRelation'),
  isInput: not('isSelect'),
  componentName: alias('field.component'),
  fieldAttrs: alias('field.attrs'),
  passThruAttrs: alias('fieldAttrs'),

  label: computed('field', 'field.options.label', function() {
    return get(this, 'field.options.label') || titlecase(get(this, 'key'));
  }),

  placeholder: computed('isSelect', function() {
    if (get(this, 'isSelect')) { return get(this, 'label'); }
    return null;
  }),
  
  choicesMap: computed('field.choices', function() {
    let choices = get(this, 'field.choices');
    let values = [];
    if (!isArray(choices)) {
      return choices || {};
    }
    let keys = Object.keys(choices);
    Object.keys(choices).forEach((k) => values.push(choices[k]));
    return _.object(keys, values);
  }),

  choicesValues: computed('field.choices', function() {
    let choices = get(this, 'field.choices');
    if (!choices) { return undefined; }
    if (isArray(choices)) {
      return choices.map((k) => k[1]);
    }
    choices = get(this, 'choicesMap');
    return Object.keys(choices).map((k) => k);
  }),

  // select related method
  getChoices: computed('options', 'choicesValues.[]', function() {
    let choices = get(this, 'choicesValues');
    let labels = get(this, 'choicesMap');
    if (Ember.isArray(choices)) { 
      return function() {
        return new Ember.RSVP.Promise(function(resolve) {
          resolve(choices.map((val) => {
            return {label: labels[val], value: val}
          }));
        });
      };
    }

    // choices is a function
    if (_.isFunction(choices)) { return choices; }

    if (get(this, 'isRelation')) {
      let type = get(this, 'field.relModel');
      return function() {
        let arr = get(this, "store").findAll(type);
        return arr.then(function(results) {
          return Ember.ArrayProxy.create({
            content: arr,
            objectAtContent: function(idx) {
              let item = get(this, 'content').objectAt(idx);
              return {
                value: item,
                label: item.get('name') //TODO: 'name' should'nt be hardcoded
              }
            }
          });
        });
      }.bind(this);
    }
  }),

  // select related method
  getChoiceLabel: computed('field', function(i) {
    let key = get(this, 'options.labelKey') || 'name';
    let isRelation = get(this, 'isRelation');
    let choices = get(this, 'choicesMap');

    return function(item) {
      if (isRelation) {
        return item.get(key);
      } else {
        if (item in choices) { 
          return choices[item];
        }
        if (_.isString(item)) {
          return item;
        }
        return item.label;
      }
    };
  }),

  fieldDidChange: observer('field', function() {
    let key = get(this, 'key');

    mixin(this, {
      rawValue: reads(`object.${key}`),
      observeErrors: observer(`object.errors.${key}.length`, `object.validations.attrs.${key}.errors.length`, function() {
        let errors = get(this, `object.errors.${key}`) || [];
        errors = errors.toArray();
        errors.concat(get(this, `object.validations.attrs.${key}.errors`) || []);
        this.set('errors', errors);
        this.set('hasErrors', errors.length > 0);
      })
    });

    if (get(this, 'isRelation')) {
      mixin(this, {
        rawValueObserver: observer(`object.${key}.id`, function() {
          this.set('rawValue', get(this, 'object.' + get(this, 'key')));
        })
      });
    }

    if (get(this, 'isSelect')) {
      mixin(this, {
        getItems: reads(`getChoices`),
        itemLabelCallback: reads(`getChoiceLabel`)
      });
    }
  }),

  value: computed('rawValue', function() {
    let serializeValue = getWithDefault(this, 'serializeValue', (value) => value);
    let raw = get(this, 'rawValue');
    if (raw instanceof Ember.ObjectProxy && get(this, 'isRelation')) {
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
    this.fieldDidChange();
  },
  
  actions: {
    updateProperty: function(value) {
      if (value instanceof Ember.ObjectProxy) {
        value.then(function(model) {
          set(get(this, 'object'), get(this, 'key'), model);
        })
      } else {
        set(get(this, 'object'), get(this, 'key'), value);
      }
    }
  }
});
