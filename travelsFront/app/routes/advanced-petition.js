import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import ENV from 'travels-front/config/environment'; 

export default Ember.Route.extend(AuthenticatedRouteMixin,{
	model(params) {

		let id=params.ap_id
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

		let startTripDate=petition.get('depart_date');
		if (startTripDate!==null){ 

			startTripDate=startTripDate.replace('Z','');
			petition.set('depart_date',startTripDate);
		}

		let endTripDate=petition.get('return_date');
		if (endTripDate!==null){ 

			endTripDate=endTripDate.replace('Z','');
			petition.set('return_date',endTripDate);
		}

		var ap_id=petition.get('advanced_info.id');
		let self=this;
		self.store.findRecord('advanced-petition', ap_id).then(function(advanced_petition) {
			var flight_id=advanced_petition.get('flight.id');
			self.store.findRecord('flight',flight_id);
			var accomondation_id=advanced_petition.get('accomondation.id');
			self.store.findRecord('accommondation',accomondation_id);
		});

		var movement_id=petition.get('movementCategory.id');
		if (movement_id!=null) {

			self.store.findRecord('movement-category',movement_id).then(function(movement_category) {
				console.log("movement-category", this.get('movement_id'))
			});
		}

		var city_code=petition.get('arrivalPoint.id');
		if (city_code!=null) {

			self.store.findRecord('city',city_code).then(function(city) {
				var country_id=city.get('country.id');
				self.store.findRecord('country',country_id).then(function(country) {
					var category_id=country.get('category.id');
					self.store.findRecord('country-category',category_id);
				});
			});
		}
	},

	setupController: function(controller, model) {
		this._super(controller, model);
		controller.set('arrivalPoints', this.store.findAll('city'));
		controller.set('countries', this.store.findAll('country'));
		controller.set('departurePoints', this.store.query('city',{ country: 10}));
		controller.set('transportations', this.store.findAll('transportation'));
		controller.set('projects', this.store.findAll('project'));
		controller.set('specialties', this.store.findAll('specialty'));
		controller.set('kinds', this.store.findAll('kind'));
		controller.set('tax-offices', this.store.findAll('taxOffice'));
		controller.set('categories', this.store.findAll('category'));
		controller.set('petition-statuses', this.store.findAll('petition-status'));
		controller.set('feedings', this.store.findAll('feeding'));
		controller.set('compensations', this.store.findAll('compensation-categories'));
		controller.set('petitionMessage','');
		controller.set('datesChanged',false);

	}
});
