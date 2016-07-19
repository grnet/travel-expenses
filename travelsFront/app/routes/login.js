import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Route.extend({
  session: Ember.inject.service('session'),

  beforeModel: function() {
    if (this.get('session.isAuthenticated')) {
      this.transitionTo('profile')
    }
  },

  model: function() {
    return this.store.createRecord('account', {
      email: 'login-user@travel.ltd',
      password: 'login'
    });
  }
});
