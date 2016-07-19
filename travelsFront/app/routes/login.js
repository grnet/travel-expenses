import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Route.extend({
  model: function() {
    return this.store.createRecord('account', {
      email: 'login-user@travel.ltd',
      password: 'login'
    });
  }
});
