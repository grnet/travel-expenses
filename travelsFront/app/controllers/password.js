import Ember from 'ember';
import ENV from 'travels-front/config/environment';

export default Ember.Controller.extend({
	session: Ember.inject.service('session'),

	actions: {

		changePassword() {
      
  		var token = this.get('session.data.authenticated.auth_token');
  		var current_password = this.get('model.current_password');
  		var new_password = this.get('model.new_password');
  		var re_new_password = this.get('model.re_new_password');
  
	    return $.ajax({
	    	method: "POST",
	      headers:{Authorization: 'Token ' + token},
	      url: ENV.APP.backend_host+"/auth/password/",
	      data: {current_password, new_password, re_new_password},
      	error: ((err) => {
      		let messageObject = JSON.parse(err.responseText);
      		var message = '';
      		for (var key in messageObject) {
      			if (key == "non_field_errors") {
      				message = message + "\n" + messageObject[key];
      			} else {
      				message = message + "\n" + key + ": " + messageObject[key];
      			}      			
      		};
        	this.set('submitError', message);       					
				}),
	    }).then(() => {
        this.transitionToRoute('profile');
 			});
    },
	}
});


