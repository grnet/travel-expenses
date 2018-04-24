import Ember from 'ember';

const DEFAULT_ROUTE = 'application-item';
const PROFILE_ROUTE = '/auth/my-profile';
const PROFILE_PARAMS = ['first_name', 'last_name', 'iban', 'specialty', 'kind', 'tax_office', 'tax_reg_num'];

function profileIsFilled(session) {
  let profile = session.get('session.authenticated');

  for (let item of PROFILE_PARAMS) {
    if (profile[item] == null) {
      return false;
    }
  }

  return true;
};

export default Ember.Route.extend({
  session: Ember.inject.service(),

  beforeModel(transition) {
    let session = this.get('session');

    if (profileIsFilled(session)) {
      this.transitionTo(DEFAULT_ROUTE);
    } else {
      this.transitionTo(PROFILE_ROUTE);
    };
  },
});
