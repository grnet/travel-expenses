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

		//let endDate=petition.get('taskEndDate');
		//if (endDate!==null) {
			////endDate=endDate.substring(0,endDate.length-1);
			//endDate=endDate.replace('Z','');
			//petition.set('taskEndDate',endDate);
		//}

		//let startDate=petition.get('taskStartDate');
		//if (startDate!==null){ 
			////startDate=startDate.substring(0,startDate.length-1);
			//startDate=startDate.replace('Z','');
			//petition.set('taskStartDate',startDate);
		//}

		var city_code=petition.get('arrivalPoint.id');
		if (city_code!=null) {
			var self=this;
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
		controller.set('editMessage','');
		controller.set('petitionNotSaved', true);

	},

	actions: {
		willTransition(transition) {
			if (this.controller.get('petitionNotSaved') && !confirm('Are you sure you want to abandon progress?Any changes will be lost unless you save them')) {
				console.log('not saved');
				transition.abort();
			} else {
				// Bubble the `willTransition` action so that
				// parent routes can decide whether or not to abort.
				console.log('saved');
				return true;
			} 
		}
	}
});
