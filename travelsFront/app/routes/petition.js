import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import ENV from 'travels-front/config/environment'; 

export default Ember.Route.extend(AuthenticatedRouteMixin,{
	model() {
		var model = this.store.createRecord('petition');
		let departureID = ENV.APP.backend_host+'/petition/city/10/';
		var rec = this.store.findRecord('city', departureID);
		rec.then(function(m) {
			model.set('departurePoint', m)
		})

		return model
	},

	afterModel(petition){

		this.store.findRecord('profile', 1).then(function(profile) {
			let pet_name=profile.get('first_name');	
			let pet_surname=profile.get('last_name');
			let pet_iban=profile.get('iban');
			let pet_specialty=profile.get('specialtyID');
			let pet_kind=profile.get('kind');
			let pet_taxNum=profile.get('taxRegNum');
			let pet_taxOffice=profile.get('taxOffice');
			let pet_category=profile.get('category');

			petition.set('name', pet_name);
			petition.set('surname',pet_surname);
			petition.set('iban', pet_iban);
			petition.set('specialtyID', pet_specialty);
			petition.set('kind', pet_kind);
			petition.set('taxRegNum', pet_taxNum);
			petition.set('taxOffice', pet_taxOffice);
			petition.set('user_category', pet_category);


		});

	},
	setupController: function(controller, model) {
		this._super(controller, model);
		controller.set('departurePoints', this.store.query('city',{ country: 10}));
		controller.set('countries', this.store.findAll('country'));
		controller.set('transportations', this.store.findAll('transportation'));
		controller.set('projects', this.store.findAll('project'));
		controller.set('specialties', this.store.findAll('specialty'));
		controller.set('kinds', this.store.findAll('kind'));
		controller.set('tax-offices', this.store.findAll('taxOffice'));
		controller.set('categories', this.store.findAll('category'));
		controller.set('petition-statuses', this.store.findAll('petition-status'));
		controller.set('petitionMessage','');
		controller.set('petitionNotSaved',true);

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
