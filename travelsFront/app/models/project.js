import DS from 'ember-data';

export default DS.Model.extend({
	name: DS.attr(),
	accountingcode: DS.attr(),
	url: DS.attr()
  
});
