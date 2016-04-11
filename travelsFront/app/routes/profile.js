import Ember from 'ember';

export default Ember.Route.extend({
	model() {
		
	return Ember.RSVP.hash({
      profile: this.store.findRecord('profile',1),
      specialty: this.store.findAll('specialty')
    });

	}
});
