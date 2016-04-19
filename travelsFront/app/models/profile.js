import Ember from 'ember';
import DS from 'ember-data';
import {validator, buildValidations} from 'ember-cp-validations';

var Validations=buildValidations({
	email: [
		validator('presence', true),
		validator('format', { type: 'email' })
	],
	taxRegNum: validator('afm-validator'),
	iban: validator('iban-validator')


});

export default DS.Model.extend(Validations,{
	'username': DS.attr(),
	'email': DS.attr(),
	'first_name': DS.attr(),
	'last_name': DS.attr(), 
	'iban': DS.attr(),
	'accountID': DS.attr(),
	'specialtyID': DS.belongsTo('specialty'),
	'kind': DS.belongsTo('kind'),
	'taxRegNum': DS.attr(),
	'taxOffice': DS.belongsTo('tax-office')

});
