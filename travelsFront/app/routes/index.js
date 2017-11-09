import Ember from 'ember';

const {
  get
} = Ember;

const DEFAULT_ROUTE = 'application-item';

export default Ember.Route.extend({
  session: Ember.inject.service(),
  beforeModel(transition) {
    this.transitionTo(DEFAULT_ROUTE);
  }
});
