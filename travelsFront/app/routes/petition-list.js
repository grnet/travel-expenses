import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin,{

	model() {
		return this.store.findAll('petition');
	},

	// setupController: function(controller, model) {
	// 	this._super(controller, model);
	// 	controller.set('petition',this.store.findAll('petition'));
	// }
});
