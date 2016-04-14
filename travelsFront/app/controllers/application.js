import Ember from 'ember';


export default Ember.Controller.extend({
	session: Ember.inject.service('session'),

	actions: {
		invalidateSession() {
			//debugger;
			var self=this;
			var token=self.get("session.data.authenticated.auth_token")
			console.log(token);
			Ember.$.ajax({
				url: "http://127.0.0.1:8000/auth/logout/",
				method: "POST", 
				headers: {"Authorization":"Token " + token}, 
				success: function(result){
					self.get('session').invalidate();
				},
				error: function(request,error){
					//console.log(this.session);
					alert("Request: "+JSON.stringify(request));
				}
			});
		}

	}

});
