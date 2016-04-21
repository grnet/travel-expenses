import Ember from 'ember';

export default Ember.Route.extend({

	// model() {
	// 	return this.store.findRecord('petition',1); 
	// },

	setupController: function(controller, model) {
		this._super(controller, model);
		controller.set('arrival-points', this.store.findAll('arrivalPoint'));
		controller.set('departure-points', this.store.findAll('departurePoint'));
		controller.set('movement-categories', this.store.findAll('movementCategory'));
		controller.set('transportations', this.store.findAll('transportation'));
		controller.set('projects', this.store.findAll('project'));
	}
});
