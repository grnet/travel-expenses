import Ember from 'ember';
import { Ability } from 'ember-can';

export default Ability.extend({
  canApprove: Ember.computed('user', function() {
  	console.log('user', this.get('name'));
    // return this.get('user.isAdmin');
  	return true;
  })
});