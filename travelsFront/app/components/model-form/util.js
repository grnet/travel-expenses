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
  'string': ['paper-input', {type: "text"}],
  'boolean': ['paper-checkbox', {}],
  'select': ['paper-select', {}],
  'date': ['paper-input', {type: "date"}],
  'datetime': ['paper-input', {type: "datetime-local"}],
  'select': ['paper-select'],
  'relation': ['paper-select']
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

  label: computed('options.label', function() {
    return get(this, 'options.label') || titlecase(get(this, 'key'));
  }),

  _component: computed('options.component', 'type', function() {
    let component = get(this, 'options.component') || TYPE_COMPONENT_MAP[get(this, 'type')];
    let type = get(this, 'type');
    Ember.assert(`Cannot resolve component for type: ${type}`, component);
    if (!isArray(component)) { component = [component, {}]; }
    component = FuncOrValue(component, this);
    return component
  }),

  component: alias('_component.0'),
  attrs: computed('options.attrs', '_component.1', function() {
    return _.extend({}, get(this, '_component.1'), get(this, 'options.attrs') || {});
  })
});


var FieldSet = Ember.Object.extend({
  fields: [],
  label: null,
  description: null
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

  fieldsets: computed('fieldsKeys.[]', 'options.fieldsets.[]', function() {
    let sets = get(this, 'options.fieldsets') || [get(this, 'fieldsKeys')];
    let fields = get(this, 'fields');
    return sets.map((set) => {
      if (isArray(set)) { 
        set = {label: null, description: null, fields: set};
      }
      let options = {label: set.label, description: set.description, fields: []};
      set.fields.forEach((key) => { options.fields.push(fields[key]); });
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
  let exclude = ui.exclude;

  let _typeFields = get(type, 'fields');
  let attrs = {};

  type.eachAttribute((k,v) => {
    let opts = _.cloneDeep(v.options);
    opts['key'] = v.name;
    opts['type'] = v.options.type || v.type || "string";
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

  let fields = _typeFields._keys.list.map((key) => {
    let options = attrs[key];
    return [key, options]
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
