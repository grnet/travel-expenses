import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin,{
	model(params) {

		var model= this.store.findRecord('petition', params.petition_id);

		//model.then(function(petition) {
		//console.log(petition.get('taskEndDate'));

		//let endDate=petition.get('taskEndDate');
		//if (endDate!==null) {

		//endDate=endDate.substring(0,endDate.length-1);
		//petition.set('taskEndDate',endDate);
		//}
		//});

		return model;
	},
	afterModel(petition){

		let endDate=petition.get('taskEndDate');
		console.log("End date:"+endDate);
		if (endDate!==null) {

			//endDate=endDate.substring(0,endDate.length-1);
			endDate=endDate.replace('Z','');
			petition.set('taskEndDate',endDate);
		}

		let startDate=petition.get('taskStartDate');

		console.log("Start date:"+startDate);
		if (startDate!==null){ 

			//startDate=startDate.substring(0,startDate.length-1);
			startDate=startDate.replace('Z','');
			petition.set('taskStartDate',startDate);
		}

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
