import Ember from 'ember';
import ENV from 'travel/config/environment';

const {
  get,
  inject,
  computed,
  computed: { reads },
} = Ember;

export default Ember.Component.extend({
  session: inject.service(),
  role: computed(function() {
    let role = get(this, 'session.session.authenticated.user_group');
    return role;
  }),
  travel_report_template: ENV.APP.links.travel_report_template,
  travel_instructions: ENV.APP.links.travel_instructions,
});
