import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';



export default Ember.Route.extend(AuthenticatedRouteMixin,{

	model() {
		
		return this.store.findAll('secretary-petition');
		//return this.store.query('petition',{status:2});
	},
	setupController: function(controller, model) {
		this._super(controller, model);
		controller.set('deleteMessage','');
		Ember.set(controller, 'created', model.created);
    Ember.set(controller, 'submitted', model.submitted);
	}
});
