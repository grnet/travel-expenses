// loadCurrentUser() {
	// 	return new RSVP.Promise((resolve, reject) => {

	// 		const accountId = this.get('session.data.authenticated.auth_token');
	// 		console.log("This is my account", accountId);

	// 		if (!Ember.isEmpty(accountId)) {
	// 			return this.get('store').findRecord('profile',accountId).then((profile) => {
	// 		  		this.set('account', profile);
	// 		  		console.log("accountid",this.get('account.user_group'));
	// 		  		resolve();
	// 			}, reject);
	// 		} else {
	// 			resolve();
	// 		}
	// 	});
	// }

import Ember from 'ember';

export default Ember.Service.extend({

	session: Ember.inject.service('session'),
	store: Ember.inject.service('store'),

  	loadCurrentUser() {
    
	    const accountId = this.get('session.data.authenticated.auth_token');
	    console.log("This is my account", accountId);
	    
	    if (!Ember.isEmpty(accountId)) {
	      
	      	this.get('store').findRecord('profile', accountId).then((profile) => {
	        	this.set('user', profile);
	        	console.log("account_group",this.get('user.user_group'));
	        	console.log("account_username",this.get('user.username'));
	      	}); 
	    }
	    return this.get('user')              
  	}
});  
