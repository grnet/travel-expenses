import Ember from 'ember';

export default Ember.Route.extend({
	model() {
		return new Ember.RSVP.Promise(function(r,e) {
			this.store.findAll('specialty').then(function() {
				r(this.store.findRecord('profile',1));
			}.bind(this))
			
		}.bind(this));
	},
	
	setupController: function(controller, model) {
    	this._super(controller, model);
    	controller.set('specialties', this.store.findAll('specialty'));
	}
});
