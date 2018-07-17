import DS from 'ember-data';

export default DS.Model.extend({
  __api__: {
    path: 'project', // ember-data would use `project*s*`
  },
  name: DS.attr(),
  accounting_code: DS.attr(),
  manager: DS.belongsTo('user', {autocomplete: true, formAttrs: { optionLabelAttr: 'full_name' }}),
  manager_id: DS.attr(),
});
