import DS from 'ember-data';

export default DS.Model.extend({
	username: DS.attr(),
	email: DS.attr(),
	first_name: DS.attr(),
	last_name: DS.attr(), 
	iban: DS.attr(),
	accountID: DS.attr(),
	specialtyID: DS.belongsTo('specialty'),
	userKind: DS.attr(),
	taxRegNum: DS.attr(),
	taxOffice: DS.attr()
  
});
