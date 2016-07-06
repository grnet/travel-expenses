import Ember from 'ember';
import DS from 'ember-data';
import {validator, buildValidations} from 'ember-cp-validations';

var Validations=buildValidations({
	username: [
		validator('presence', true)
		//validator('unique-username')
	
	],
	password: [
		validator('presence', true),
		validator('length', {
			min: 4,
			max: 8
		})
	],
	email: [
		validator('presence', true),
		validator('format', { type: 'email' })
	]
});

export default DS.Model.extend(Validations,{
	'username': DS.attr('string'),
	'password': DS.attr('string', {fieldAttrs: {type: 'password'}}), 
	'email': DS.attr('string')
});




