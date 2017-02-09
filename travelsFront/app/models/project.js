import DS from 'ember-data';

export default DS.Model.extend({
  __api__: {
    ns: '/'
  },
  full_label: Ember.computed('name', function(){
    return this.get('name') + " (" + this.get('manager_name') + " " + this.get('manager_surname') + ")"
  }),
	name: DS.attr(),
	accountingCode: DS.attr(),
	manager_name: DS.attr(),
	manager_surname: DS.attr(),
	manager: DS.attr(),
	url: DS.attr()
});
