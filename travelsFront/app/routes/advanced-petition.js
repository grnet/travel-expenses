import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import ENV from 'travels-front/config/environment'; 

export default Ember.Route.extend(AuthenticatedRouteMixin,{
	model(params) {

		let id=params.petition_id
		id=ENV.APP.backend_host+'/petition/user_petition/'+id
		var model= this.store.findRecord('petition', id);

		return model;

	},

	afterModel(petition){

		let endDate=petition.get('taskEndDate');
		if (endDate!==null) {

			//endDate=endDate.substring(0,endDate.length-1);
			endDate=endDate.replace('Z','');
			petition.set('taskEndDate',endDate);
		}

		let startDate=petition.get('taskStartDate');

		if (startDate!==null){ 

			//startDate=startDate.substring(0,startDate.length-1);
			startDate=startDate.replace('Z','');
			petition.set('taskStartDate',startDate);
		}
		var ap_id=petition.get('advanced_info.id');
		let self=this;
		self.store.findRecord('advanced-petition', ap_id).then(function(advanced_petition) {
			var flight_id=advanced_petition.get('flight.id');
			self.store.findRecord('flight',flight_id);
			var accomondation_id=advanced_petition.get('accomondation.id');
			self.store.findRecord('accommondation',accomondation_id);
		});
	},

	setupController: function(controller, model) {
		this._super(controller, model);
		controller.set('arrivalPoints', this.store.findAll('city'));
		controller.set('countries', this.store.findAll('country'));
		controller.set('departurePoints', this.store.query('city',{ country: 10}));
		controller.set('movement-categories', this.store.findAll('movementCategory'));
		controller.set('transportations', this.store.findAll('transportation'));
		controller.set('projects', this.store.findAll('project'));
		controller.set('specialties', this.store.findAll('specialty'));
		controller.set('kinds', this.store.findAll('kind'));
		controller.set('tax-offices', this.store.findAll('taxOffice'));
		controller.set('categories', this.store.findAll('category'));
		controller.set('petition-statuses', this.store.findAll('petition-status'));
		//controller.set('advanced-petitions', this.store.findAll('advanced-petition'));
		//controller.set('accommondations', this.store.findAll('accommondation'));
		//controller.set('flights', this.store.findAll('flight'));
		controller.set('feedings', this.store.findAll('feeding'));
		controller.set('compensations', this.store.findAll('compensation-categories'));
		controller.set('editMessage','');

	}
});
