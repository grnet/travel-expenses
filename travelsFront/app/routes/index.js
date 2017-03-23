import Ember from 'ember';

const {
  get
} = Ember;

const DEFAULT_ROUTE = 'auth.profile';

export default Ember.Route.extend({
  session: Ember.inject.service(),
  beforeModel(transition) {
    if (get(this, 'session.session.isAuthenticated')) {
      transition.abort();
      this.transitionTo(DEFAULT_ROUTE);
    }
  }
});