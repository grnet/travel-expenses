import Ember from 'ember';

export default Ember.Route.extend({

	 model() {
		 //return this.store.findRecord('petition',1); 
		 //console.log(this.store.findAll('petition').get('id'))
		 return this.store.findAll('petition');
	 },

	setupController: function(controller, model) {
		this._super(controller, model);
		controller.set('arrival-points', this.store.findAll('arrivalPoint'));
		controller.set('departure-points', this.store.findAll('departurePoint'));
		controller.set('movement-categories', this.store.findAll('movementCategory'));
		controller.set('transportations', this.store.findAll('transportation'));
		controller.set('projects', this.store.findAll('project'));
		controller.set('specialties', this.store.findAll('specialty'));
		controller.set('kinds', this.store.findAll('kind'));
		controller.set('tax-offices', this.store.findAll('taxOffice'));
	}
});
