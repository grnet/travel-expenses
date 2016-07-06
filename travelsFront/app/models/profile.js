import Ember from 'ember';
import DS from 'ember-data';
import {validator, buildValidations} from 'ember-cp-validations';


var Validations=buildValidations({
   email: [
       validator('presence', true),
       validator('format', { type: 'email' })
   ],
   taxRegNum: validator('afm-validator'),
   iban: validator('iban-validator'),
   first_name: [validator('length', {min: 1}), validator('presence', true)],
   last_name: [validator('length', {min: 1}), validator('presence', true)],
   taxRegNum: [validator('length', {min: 1}), validator('presence', true)]
});

export default DS.Model.extend(Validations, {
	'username': DS.attr(),
	'email': DS.attr({hint: 'A valid email address'}),
	'first_name': DS.attr(),
	'last_name': DS.attr(), 
	'iban': DS.attr(),
	'accountID': DS.attr({'label': 'Account'}),
	'specialtyID': DS.belongsTo('specialty'),
	'kind': DS.belongsTo('kind'),
	'taxRegNum': DS.attr(),
	'taxOffice': DS.belongsTo('tax-office'),
	'category': DS.belongsTo('category'),
	'user_group': DS.attr()
});
