import Ember from 'ember';

export default Ember.Route.extend({

	model() {
		return this.store.findAll('petition');
	},

	// setupController: function(controller, model) {
	// 	this._super(controller, model);
	// 	controller.set('petition',this.store.findAll('petition'));
	// }
});
