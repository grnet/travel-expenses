import Ember from 'ember';
import DS from 'ember-data';
import {validator, buildValidations} from 'ember-cp-validations';


var Validations=buildValidations({
  email: [
    validator('presence', true),
    validator('format', { type: 'email' })
  ],
  iban: validator('iban-validator'),
  first_name: [
    validator('presence', true),
    validator('length', {min: 1})
  ],
  last_name: [
    validator('presence', true),
    validator('length', {min: 1})
  ],
  taxRegNum: [
    validator('presence', true),
    validator('length', {min: 1}),
    validator('afm-validator')
  ]
});

export default DS.Model.extend(Validations, {
  __ui__: {
    'default': {
      fieldsets: [
        {
          'label': 'My account',
          'fields': ['username', 'email']
        },
        {
          'label': 'Personal info',
          'fields': ['first_name', 'last_name', 'specialtyID', 'kind','taxRegNum', 'taxOffice', 'iban', 'category']
        }
      ],
      layout: {
        flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
      }
    }
  },

	'username': DS.attr({attrs: {readonly: true}}),
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
