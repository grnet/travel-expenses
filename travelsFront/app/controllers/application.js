import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Controller.extend({

	session: Ember.inject.service('session'),
	
	actions: {
		
		invalidateSession() {
			
			var self=this;
			var token=self.get("session.data.authenticated.auth_token");
			
			Ember.$.ajax({
				url: ENV.APP.backend_host+"/auth/logout/",
				method: "POST", 
				headers: {"Authorization":"Token " + token}, 
				success: function(result){
					self.get('session').invalidate();
				},
				error: function(request,error){
					alert("Request: " + JSON.stringify(request));
				}
			});
		}

	}

});
