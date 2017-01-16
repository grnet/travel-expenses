import Ember from 'ember';

export default Ember.Route.extend({

	resetController: function(controller) {
    controller.set('submitError', '');
  },

	model: function() {
    return this.store.createRecord('password')
  }
});
