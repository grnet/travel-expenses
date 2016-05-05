import DS from 'ember-data';

export default DS.Model.extend({
	name: DS.attr(),
	accountingCode: DS.attr(),
	url: DS.attr()
  
});
