import Ember from 'ember';

export default Ember.Route.extend({
	model() {
		return this.store.findRecord('profile',1); 
	},

	setupController: function(controller, model) {
		this._super(controller, model);
		controller.set('specialties', this.store.findAll('specialty'));
		controller.set('kinds', this.store.findAll('kind'));
		controller.set('tax-offices', this.store.findAll('taxOffice'));
	}
});
