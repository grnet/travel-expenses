import Ember from 'ember';

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
});
