import Ember from 'ember';
import DS from 'ember-data';
import {validator, buildValidations} from 'ember-cp-validations';

const LOGIN_UI = {
  exclude: ['email', 'password'],
  extra_fields: [
    ['login_pass', 
      {
        type: 'string',
        attrs: {type: 'password', required: true}
      }
    ]
  ],
  layout: {
    flex: [50, 50, 50, 50]
  }
};

const SIGNUP_UI = {}


var Validations=buildValidations({
	username: [
		validator('presence', true)
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

export default DS.Model.extend(Validations, {
  __api__: {
    ns: 'auth',
    path: 'register'
  },
  __ui__: {
    'signup': SIGNUP_UI,
    'login': LOGIN_UI
  },

	'username': DS.attr('string', {attrs: {required: true}}),
	'password': DS.attr('string', {attrs: {type: 'password'}}), 
	'email': DS.attr('string')
});
