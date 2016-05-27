import Ember from 'ember';
import { Ability } from 'ember-can';

export default Ability.extend({
  canApprove: Ember.computed('user.isAdmin', function() {
  	console.log('user.isAdmin')
    return this.get('user.isAdmin');
  })
});