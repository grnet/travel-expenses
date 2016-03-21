import DS from 'ember-data';

export default DS.Model.extend({ 
	name: DS.attr(),
	surname: DS.attr(), 
	iban: DS.attr(),
	accountID: DS.attr(),
	specialtyID: DS.attr(),
	userKind: DS.attr(),
	taxRegNum: DS.attr(),
	taxOffice: DS.attr()
	      
});
