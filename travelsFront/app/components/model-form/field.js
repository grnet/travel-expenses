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
  fieldAttrs: alias('field.attrs'),
  componentName: alias('field.component'),
  isRelation: equal('field.type', 'relation'),

  label: computed('field', 'field.options.label', function() {
    return get(this, 'field.options.label') || titlecase(get(this, 'key'));
  }),

  placeholder: computed('isSelect', function() {
    return get(this, 'field.attrs.placeholder') || get(this, 'label');
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
