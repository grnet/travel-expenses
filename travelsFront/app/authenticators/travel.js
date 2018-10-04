import Ember from 'ember';
import ApimasAuthenticator from 'ember-gen-apimas/authenticators/apimas';

const {
  merge,
} = Ember;

export default ApimasAuthenticator.extend({
  profilePath: '/auth/me/detailed/',
  processProfileData(data, profile) {
    if (!data['role']) {
      data['role'] = 'anonymous';
      if (profile.hasOwnProperty('user_group')) {
        data['role'] = profile.user_group;
      }
    }
    merge(data, profile);

    return data;
  },
});
