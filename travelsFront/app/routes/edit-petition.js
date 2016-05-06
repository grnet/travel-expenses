import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin,{
	model(params) {
		return this.store.findRecord('petition', params.petition_id);
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
		controller.set('petition-statuses', this.store.findAll('petition-status'));
		//controller.set('profile',this.store.findRecord('profile',1));

	}
});
