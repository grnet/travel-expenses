import Ember from 'ember';


export default Ember.Controller.extend({
	session: Ember.inject.service('session'),

	actions: {

		invalidateSession() {

    		Ember.$.ajax({
    			url: "http://127.0.0.1:8000/auth/logout/",
    			method: "POST", 
    			headers: {"Authorization":"Token" + " 30afe8921b6aff3dee130976ed8ca40e3613ae52"}, 
    			success: function(result){
    				this.get('session').invalidate();
    			},
    			error: function(request,error){
    				console.log(this.session);
        			alert("Request: "+JSON.stringify(request));
    			}
    		});
    	}
	}
	
});
