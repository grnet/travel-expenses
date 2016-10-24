import Ember from 'ember';
import DS from 'ember-data';
import {validator, buildValidations} from 'ember-cp-validations';


var Validations=buildValidations({

	new_password: [
		validator('presence', true),
		validator('length', {
			min: 4
		})
	]
});

const PASSWORD = {
  fieldsets: [
	  {
	    'label': 'my_account.label',
	    'fields': ['current_password', 'new_password', 're_new_password']
	  }
	],
	layout: {
  	flex: [100, 100, 100]
	}
};


export default DS.Model.extend(Validations, {
  __api__: {
    ns: 'auth',
    path: 'password'
  },
  __ui__: {
    'password': PASSWORD,
  },

	'current_password': DS.attr('string', {attrs: {type: 'password'}}), 
	'new_password': DS.attr('string', {attrs: {type: 'password'}}), 
	're_new_password': DS.attr('string', {attrs: {type: 'password'}}), 
});
