import Ember from 'ember';
import ApplicationRouteMixin from 'ember-simple-auth/mixins/application-route-mixin';

export default Ember.Route.extend(ApplicationRouteMixin,{
	user: null,

	beforeModel(){
    	let user = this.get("account").loadCurrentUser();
	},	
});
