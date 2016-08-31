import Ember from 'ember';
import DS from 'ember-data';
import {validator, buildValidations} from 'ember-cp-validations';
import ENV from 'travels-front/config/environment'; 

const CHOICES = ENV.APP.resource_choices;


var Validations=buildValidations({
  email: [
    validator('presence', {presence: true}),
    validator('format', { type: 'email' })
  ],
  iban: validator('iban-validator'),
  first_name: [
    validator('presence', {presence: true}),
    validator('length', {min: 2})
  ],
  last_name: [
    validator('presence', true),
    validator('length', {min: 2})
  ],
  tax_reg_num: [
    validator('presence', {presence: true}),
    validator('number', {allowString: true, integer: true}),
    validator('length', {is: 9}),
  ]
});

const UI_DEFAULT = {
  fieldsets: [
    {
      'label': 'my_account.label',
      'fields': ['username', 'email', 'first_name', 'last_name']
    },
    {
      'label': 'personal_info.label',
      'fields': ['specialty', 'kind', 'tax_reg_num', 'tax_office', 'iban', 'user_category']
    }
  ],
  layout: {
    flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
  }
};


export default DS.Model.extend(Validations, {
  __api__: {
    ns: 'auth',
    path: 'me/detailed',
    buildURL: function(adapter, url, id, snap, rtype, query) {
      // always return my profile endpoint
      return this.urlJoin(adapter.get('host'), this.ns, this.path) + '/';
    }
  },

  __ui__: {
    'default': UI_DEFAULT
  },
  
	'username': DS.attr({
    attrs: {
      disabled: true
    }
  }),
	'email': DS.attr({
    hint: 'hint_email.label'
  }),
	'first_name': DS.attr(),
	'last_name': DS.attr(), 
	'iban': DS.attr(),
	'specialty': DS.attr({
    'choices': CHOICES.SPECIALTY
  }),
	'kind': DS.attr({
    'choices': CHOICES.KIND
  }),
	'tax_reg_num': DS.attr(),
	'tax_office': DS.belongsTo('tax-office', {
    attrs:{
      autocomplete: true,
    }
  }),
	'user_category': DS.attr({
    'attrs': { disabled: true, readonly: true}, 
    'choices': CHOICES.USER_CATEGORY
  }),
  'user_group': DS.attr(),
});
