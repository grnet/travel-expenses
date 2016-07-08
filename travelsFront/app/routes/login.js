import Ember from 'ember';

export default Ember.Route.extend({
  model: function() {
    return this.store.createRecord('account', {
      email: 'login-user@travel.ltd',
      password: 'login'
    });
  }
});
