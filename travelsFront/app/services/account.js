import Ember from 'ember';

export default Ember.Service.extend({

	session: Ember.inject.service('session'),
	store: Ember.inject.service('store'),

  loadCurrentUser() {

	    const accountId = this.get('session.data.authenticated.auth_token');
	    
	    if (!Ember.isEmpty(accountId)) {
	    	return this.get('store').findRecord('profile', accountId).then((profile) => {
	      	this.set('user', profile);
	      	return profile;
	    	});
	    }
 			return Ember.RSVP.resolve(this.get('user'));	    	                
  	}
});  
