import DS from 'ember-data';

export default DS.Model.extend({
  __api__: {
    path: 'project', // ember-data would use `project*s*`
  },
  name: DS.attr(),
  accounting_code: DS.attr(),
  manager_name: DS.attr(),
  manager_surname: DS.attr(),
  manager_email: DS.attr(),
});
