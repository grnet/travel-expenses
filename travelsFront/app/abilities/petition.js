import Ember from 'ember';
import { Ability } from 'ember-can';

export default Ability.extend({

	canApprove: Ember.computed('account.user.user_group', function() {
    	console.log("This is my permission group ", this.get('account.user.user_group'))
    	return this.get('account.user.user_group') === "SECRETARY";
	})
});