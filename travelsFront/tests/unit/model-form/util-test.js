import { module } from 'qunit';
import { test } from 'ember-qunit';
import { 
  ResourceMeta,
  Field,
  FieldSet,
  ResourceMetaFrom
} from 'travels-front/components/model-form/util';
import Ember from 'ember';
import DS from 'ember-data';


module('model-form/util');

const {
  get, set
} = Ember;

const META1 = {
  fields: [['username', {'type': 'string'}], ['password', {'type': 'string'}]]
};

const META2 = {
  fields: [['username', {'type': 'string'}], ['password', {'type': 'string'}]],
  fieldsets: [
    ['username'],
    {
      'label': 'label2',
      'fields': ['password']
    }
  ]
};

test('should initialize properly', function(assert) {
  assert.raises(function() { let meta = new ResourceMeta(); }, "no options raises error");
  assert.raises(function() { let meta = new ResourceMeta({fields: {object: {}}});}, "no fields raises error");

  let meta = new ResourceMeta({options: META1});
  assert.ok(meta, "meta initialized");

  assert.equal(meta.get('fieldsListRaw.length'), 2, "fieldsListRaw.length is 2");
  assert.equal(meta.get('fieldsList.length'), 2, "fieldsList.length is 2");

  assert.ok(meta.get('fields'), "fields are set");
  assert.ok(meta.get('fields.username'), "username field is set");
  assert.ok(meta.get('fields.username') instanceof Field, "username field is Field");
});


test('fieldsets computed', function(assert) {
  let meta = new ResourceMeta({options: META1});
  assert.equal(meta.get('fieldsets.length'), 1);
  let fs = meta.get('fieldsets')[0];
  assert.ok(fs instanceof FieldSet);
  assert.equal(fs.get('fields.length'), 2);

  meta = new ResourceMeta({options: META2});
  assert.equal(meta.get('fieldsets.length'), 2);
  fs = meta.get('fieldsets')[1];
  assert.equal(fs.get('label'), 'label2');
  assert.ok(fs instanceof FieldSet);
  assert.equal(fs.get('fields.length'), 1);
});

test('field defaults', function(assert) {
  let options;
  let field = function(attrs) { return new Field({options: attrs}); };

  assert.raises(function() { return field({}); }, 'valid params required');
  assert.raises(function() { return field({'type': 'string'}); }, 'key is required');

  let f1 = field({key: 'username', type: 'string'});
  assert.equal(get(f1, 'label'), 'Username');
  assert.equal(get(f1, 'attrs.type'), 'text');
  assert.equal(get(f1, 'component'), 'paper-input');

  let f2 = field({key: 'username', type: 'string', component: 'custom-component'});
  assert.equal(get(f2, 'attrs.type'), null);
  assert.equal(get(f2, 'component'), 'custom-component');
  assert.equal(Object.keys(get(f2, 'attrs')).length, 0);

  let f3 = field({
    key: 'username',
    type: 'string',
    component: ['custom-component', {'attr1': 1, 'attr2': 2}]
  });
  assert.deepEqual(get(f3, 'attrs'), {'attr1': 1, 'attr2': 2});
});


test('ember model', function(assert) {
  let Model = DS.Model.extend({
    username: DS.attr(),
    fullname: DS.attr('string'),
    isAdmin: DS.attr('boolean'),
    bornAt: DS.attr('string', {attrs: {type: 'date'}}),
    created: DS.attr('date'),
    category: DS.attr('string', {type: 'select'}),
    project: DS.belongsTo('project')
  });

  let meta = ResourceMetaFrom(Model);
  assert.equal(get(meta, 'fields.fullname.type'), 'string', 'fullname type is string');
  assert.equal(get(meta, 'fields.bornAt.attrs.type'), 'date', 'bornAt component attr is set to date');
  assert.equal(get(meta, 'fields.bornAt.type'), 'string', 'bornAt type is string');
  assert.equal(get(meta, 'fields.created.type'), 'date', 'created type is date');
  assert.equal(get(meta, 'fields.created.component'), 'paper-input', 'created component is paper-input');
  assert.equal(get(meta, 'fields.created.attrs.type'), 'date', 'created component type is date');
  assert.equal(get(meta, 'fields.category.type'), 'select', 'category type is select');
  assert.equal(get(meta, 'fields.project.type'), 'relation', 'project is relation');

  let Model2 = Model.extend({});
  Model2.__ui__ = {default: {
    extra_fields: [['extra_field', {type: 'string'}]],
    exclude: ['bornAt']
  }};
  
  let meta2 = ResourceMetaFrom(Model2);
  assert.equal(get(meta2, 'fields.bornAt'), undefined, 'bornAt field is excluded');
  assert.equal(get(meta2, 'fields.extra_field.type'), 'string', 'extra_field field is appended');
});

test('field layout', function(assert) {
  let options = {
    fields: [
      ['field1', {type: 'string'}],
      ['field2', {type: 'string', layout: {icon: 'warn'}}]
    ],

    layout: {
      flex: [20, 80],
      classNames: {
        'field1': 'field1-class',
        'field2': 'field2-class'
      }
    }
  };

  let meta = new ResourceMeta({options: options});
  assert.equal(meta.get('fieldsList.0.layout.flex'), 20, 'field1 flex layout set');
  assert.equal(meta.get('fieldsList.1.layout.flex'), 80, 'field2 flex layout set');
  assert.equal(meta.get('fieldsList.1.layout.icon'), 'warn', 'field2 extra icon layout set');
  set(meta, 'fieldsList.0.layout.flex', 30);
  assert.equal(meta.get('fieldsList.0.layout.flex'), 30, 'field1 flex layout modified');
});
