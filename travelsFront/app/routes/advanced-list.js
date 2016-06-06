import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';



export default Ember.Route.extend(AuthenticatedRouteMixin,{

	model() {
		
		return this.store.findAll('petition');
		//return this.store.query('petition',{status:2});
	},
	setupController: function(controller, model) {
		this._super(controller, model);
		controller.set('deleteMessage','');
	}
});
