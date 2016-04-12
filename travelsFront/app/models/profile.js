import DS from 'ember-data';

export default DS.Model.extend({
	username: DS.attr(),
	email: DS.attr(),
	first_name: DS.attr(),
	last_name: DS.attr(), 
	iban: DS.attr(),
	accountID: DS.attr(),
	specialtyID: DS.belongsTo('specialty'),
	kind: DS.belongsTo('kind'),
	taxRegNum: DS.attr(),
	taxOffice: DS.belongsTo('tax-office')

});
