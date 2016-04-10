import Ember from 'ember';

export default Ember.Controller.extend({
	
	session: Ember.inject.service('session'),

  	actions: {
    	authenticate: function() {
	      	var credentials = this.getProperties('identification', 'password'),
	        authenticator = 'authenticator:token';

	      	this.get('session').authenticate(authenticator, credentials).catch((reason) => {
        		this.set('errorMessage', reason.error || reason);
        	});

    	}
  	}
});
