import Ember from 'ember';
import BaseValidator from 'ember-cp-validations/validators/base';

export default BaseValidator.extend({
	store: Ember.inject.service(),

	validate(value/*, options, model, attribute*/) {
		return this.get('store').query('account',{username:value}).then(result => {return Ember.isEmpty(result)? true : 'The username ${value} already exists';});
	}
});
