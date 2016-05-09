import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin,{

	//entriesSorting: ['creationDate:desc'],
	//collection: Ember.computed.sort('entries', 'entriesSorting')
	model() {
		
		return this.store.findAll('petition');
	}
	//afterModel(petitions){

		//console.log("Petitions unsorted"+petitions);

		//petitions=petitions.sortBy('creationDate');
		
		//petitions=petitions.sortBy('iban');

		//console.log("Petitions sorted"+petitions);
		//return petitions;
	//}

	// setupController: function(controller, model) {
	// 	this._super(controller, model);
	// 	controller.set('petition',this.store.findAll('petition'));
	// }
});
