import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Controller.extend({

	session: Ember.inject.service('session'),

	actions: {

		invalidateSession() {

			var token = this.get("session.data.authenticated.auth_token");

			Ember.$.ajax({
				url: ENV.APP.backend_host+"/auth/logout/",
				method: "POST", 
				headers: {"Authorization":"Token " + token}, 
				success: function(result){
					this.get('session').invalidate();
        }.bind(this),
				error: function(request,error){
					alert("Request: " + JSON.stringify(request));
				}
			});
		}

	}

});
