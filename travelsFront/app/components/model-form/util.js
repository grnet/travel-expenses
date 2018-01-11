import Ember from 'ember';
import DS from 'ember-data';
import _ from 'lodash/lodash';

const {
  String: { capitalize, decamelize }
} = Ember;
const WORD_SEPERATORS = new RegExp('[-_\. ]', 'g');
export const titlecase = (string) =>
  decamelize(string)
    .split(WORD_SEPERATORS)
    .map((w) => capitalize(w))
    .join(' ');


const {
  computed,
  computed: { alias },
  observer,
  assert,
  set,
  get,
  merge,
  isEmpty,
  isArray
} = Ember;

const isFunction = function(s) {
  return typeof s === 'function';
}

function FuncOrValue(subj, ...args) {
  if (isFunction(subj)) {
    return subj(...args)
  }
  return subj;
};

const TYPE_COMPONENT_MAP = {
  'string': ['model-form/fields/input', {type: "text"}],
  'boolean': ['model-form/fields/checkbox', {}],
  'select': ['model-form/fields/select', {}],
  'date': ['model-form/fields/date', {time: false}],
  'date-simple': ['model-form/fields/date', {time: false}],
  'number': ['model-form/fields/input', {type: "text"}],
  'datetime': ['model-form/fields/date', {time: 'local'}],
  'select': ['model-form/fields/select'],
  'file': ['model-form/fields/file'],
  'relation': ['model-form/fields/select'],
  'autocomplete': ['model-form/fields/autocomplete']
};

var Field = Ember.Object.extend({
  init() {
    this._super();
    let key = get(this, 'key');
    let opts = get(this, 'options');
    let type = get(this, 'type');

    Ember.assert(`key is required for ${opts}`, key);
    Ember.assert(`type is required for ${key}`, type);
  },

  options: {},
  key: alias('options.key'),
  type: alias('options.type'),
  layout: alias('options.layout'),
  relType: alias('options.relType'),
  relModel: alias('options.relModel'),
  choices: alias('options.choices'),

  label: computed('options.label', function() {
    return get(this, 'options.label') || titlecase(get(this, 'key'));
  }),

  resolveComponent: function(type, attrs) {
    if ((type == 'select' || type == 'relation') && attrs.autocomplete) {
      type = 'autocomplete';
    }
    let component = get(this, 'options.component') || TYPE_COMPONENT_MAP[type];
    Ember.assert(`Cannot resolve component for type: ${type}`, component);
    if (!isArray(component)) { component = [component, {}]; }
    component = FuncOrValue(component, this);
    return component
  },

  _component: computed('options.component', 'type', function() {
    let type = get(this, 'type');
    let attrs = get(this, 'options.attrs') || {};
    return this.resolveComponent(type, attrs);
  }),

  component: alias('_component.0'),
  attrs: computed('options.attrs', '_component.1', function() {
    return _.extend({}, get(this, '_component.1'), get(this, 'options.attrs') || {});
  })
});


var FieldSet = Ember.Object.extend({
  fields: [],
  label: null,
  text: null,
  flat: null
});


var ResourceMeta = Ember.Object.extend({

  init: function(args) {
    this._super();
    let options = get(this, 'options');
    Ember.assert('options.fields is required', options && options.fields);
    Ember.assert('options.fields should be an array', isArray(options.fields));
  },

  layout: alias('options.layout'),
  exclude: alias('options.exclude'),
  fieldsListRaw: alias('options.fields'),
  fieldsLayout: computed('options.layout', 'fieldsListRaw', function() {
    let layout = get(this, 'layout') || {};
    let keys = Object.keys(layout);
    let parsedLayout = {};
    keys.forEach((k) => {
      let opt = layout[k];
      if (isArray(opt)) {
        opt.forEach((v, i) => {
          let _opt = {}; _opt[k] = v;
          parsedLayout[i] = merge(merge({}, (parsedLayout[i] || {})), _opt);
        });
      } else {
        Object.keys(opt).forEach((fk) => {
          let _opt = {}; _opt[k] = opt[fk];
          parsedLayout[fk] = merge(merge({}, (parsedLayout[fk] || {})), _opt);
        });
      }
    });
    return parsedLayout;
  }),

  fieldsList: computed('fieldsListRaw.[]', 'exclude.[]', 'fieldsLayout', function() {
    let excluded = get(this, 'exclude') || [];
    let fieldsLayout = get(this, 'fieldsLayout');
    return get(this, 'fieldsListRaw').map((fieldEntry, i) => {
      let options = _.extend({}, fieldEntry[1] || {});
      options.key = fieldEntry[0];
      options.layout = merge(
        merge(
          merge({}, options.layout || {}), 
          fieldsLayout[i]), 
        fieldsLayout[options.key]);
      if (excluded.indexOf(options.key) > -1) { return false; }
      return new Field({options});
    }).filter((e) => e);
  }),

  fieldsKeys: computed('fieldsList.[]', function() {
    return get(this, 'fieldsList').map((i) => get(i, 'key'));
  }),

  fields: computed('fieldsList.[]', function() {
    let fieldsMap = {};
    get(this, 'fieldsList').forEach((field) => {
      fieldsMap[field.get("key")] = field;
    });
    return fieldsMap;
  }),

  fieldsets: computed('fields.[]', 'options.fieldsets.[]', function() {
    let sets = get(this, 'options.fieldsets') || [{fields: get(this, 'fieldsKeys')}];
    let flat = !get(this, 'options.fieldsets');
    let fields = get(this, 'fields');
    return sets.map((set) => {
      let layout = merge({}, set.layout || {});
      if (isArray(set)) { 
        set = {label: null, text: null, fields: set, flat: flat};
      }
      let options = {
        label: set.label, text: set.text, fields: [], flat: set.flat || flat
      };
      set.fields.forEach((key, i) => {
        if (!key) { return; }
        let field;
        let r = key;
        if (isArray(key)) {
          field = fields[key[0]];
          field.options = merge({}, merge(field.options, key[1]));
          key = key[0];
        } else {
          field = fields[key];
        }
        assert(`Cannot resolve field ${key}`, field);
        field.options.layout = field.options.layout || {};
        Object.keys(layout).forEach((lk) => {
          let layoutObject = layout[lk];
          if (isArray(layoutObject)) {
            if (layoutObject[i] !== undefined) {
              field.options.layout[lk] = layoutObject[i]
            }
          }
        });
        options.fields.push(field);
      });

      return new FieldSet(options);
    });
  })
});


const ResourceMetaFromModel = function(type, nsKey='default', ns='__ui__') {
  if (type instanceof DS.Model) { type = type.constructor; }
  let uis = type.prototype[ns] || type[ns] || {};
  let ui = uis[nsKey] || {};
  let extra = ui.extra_fields || [];
  let fieldsets = ui.fieldsets || null;
  let layout = ui.layout || {};
  let exclude = ui.exclude || [];

  let _typeFields = get(type, 'fields');
  let fields = ui.fields || [];
  fields = fields.concat();
  let attrs = {};

  type.eachAttribute((k,v) => {
    let opts = _.cloneDeep(v.options);
    opts['key'] = v.name;
    if (!v.options.type && v.options.choices) {
      v.options.type = 'select';
    }
    opts['type'] = v.options.type || v.type || 'string';
    attrs[k] = opts; 
  });

  type.eachRelationship((k,v) => {
    let opts = _.cloneDeep(v.options);
    opts['key'] = v.key;
    opts['relType'] = v.kind;
    opts['relModel'] = v.type;
    opts['type'] = 'relation';
    attrs[k] = opts;
  });

  if (!fields.length) {
    fields = _typeFields._keys.list.concat();
    if (exclude.length) {
      exclude.forEach((f) => {
        fields.removeObject(f);
      })
    }
  }

  fields.forEach((field, i) => {
    let _key = field;
    if (isArray(field)) {
      _key = field[0]
      if (attrs[_key]) {
        field[1] = merge({}, merge(attrs[_key], field[1]));
      }
    } else {
      fields[i] = [field, merge({}, attrs[field] || {
        type: 'virtual'
      })];
    }
  });

  fields = fields.concat(extra);
  let meta = {fields, exclude, fieldsets, layout};
  return new ResourceMeta({options: meta});
}


const ResourceMetaFrom = function(subj, meta, nsKey='default', ns='__ui__') {
  if (meta && !isEmpty(meta)) { return new ResourceMeta({options: meta}); }
  if (subj instanceof DS.Model || subj.prototype instanceof DS.Model) {
    return ResourceMetaFromModel(subj, nsKey, ns);
  }
  let repr = subj && subj.toString();
  Ember.assert("Cannot resolve resource meta for `{repr}`", false);
}

export {ResourceMeta, Field, FieldSet, ResourceMetaFrom};
