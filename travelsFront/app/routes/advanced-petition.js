import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend({

// export default Ember.Route.extend(AuthenticatedRouteMixin,{
	// model(params) {
	// 	console.log("model id " + params.petition_id);
	// 	var model= this.store.findRecord('advanced-petition', params.advancedPetition_id);

	// 	return model;
	// },
});
