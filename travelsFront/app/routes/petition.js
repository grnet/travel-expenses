import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin,{
	model() {
		return this.store.createRecord('petition');
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
		//controller.set('arrivalPoints', this.store.findAll('city'));
		controller.set('countries', this.store.findAll('country'));
		controller.set('movement-categories', this.store.findAll('movementCategory'));
		controller.set('transportations', this.store.findAll('transportation'));
		controller.set('projects', this.store.findAll('project'));
		controller.set('specialties', this.store.findAll('specialty'));
		controller.set('kinds', this.store.findAll('kind'));
		controller.set('tax-offices', this.store.findAll('taxOffice'));
		controller.set('categories', this.store.findAll('category'));
		controller.set('petition-statuses', this.store.findAll('petition-status'));
		controller.set('petitionMessage','');
		
	},
	// deactivate: function() {
 //    	this.modelFor("petition").get("transaction").rollback();
 //    	alert('Please save before leave. If you leave now no changes will be saved');
 //  	},
  	actions: {
	    willTransition(transition) {
	    	this.controller.get('model').rollbackAttributes();
	    	alert('Please save before leave. If you leave now no changes will be saved');
	      // if (this.controller.get('here i should catch the save success action') &&
	      //     !confirm('Are you sure you want to abandon progress?')) {
	      //   transition.abort();
	      // } else {
	      //   // Bubble the `willTransition` action so that
	      //   // parent routes can decide whether or not to abort.
	      //   return true;
	      // }
	    }
  	}
});
