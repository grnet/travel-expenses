import Ember from 'ember';
import { Ability } from 'ember-can';

export default Ability.extend({

  canApprove: Ember.computed('account.user.user_group', function() {
      return this.get('account.user.user_group') === "SECRETARY";
  }),
  canSee: Ember.computed('account.user.user_group', function() {
      return this.get('account.user.user_group') === "USER";
  }),
  canCompensate: Ember.computed('account.user.user_group', function() {
      return this.get('account.user.user_group') === "CONTROLLER";
  }),
  canManagerApprove: Ember.computed('account.user.user_group', function() {
    return this.get('account.user.user_group') === "MANAGER";
  }),
  canView: Ember.computed('account.user.user_group', function() {
    return this.get('account.user.user_group') === "VIEWER";
  }),
  canPresidentApprove: Ember.computed('account.user.user_group', function() {
    return this.get('account.user.user_group') === "PRESIDENT_SECRETARY";
  }),
});
