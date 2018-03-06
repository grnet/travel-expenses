import Ember from 'ember';
import ApimasAuthenticator from 'ember-gen-apimas/authenticators/apimas';

const {
  merge
} = Ember;

export default ApimasAuthenticator.extend({
  profilePath: '/auth/me/detailed',
  processProfileData(data, profile) {
    data['role'] = 'anonymous';
    if (data.hasOwnProperty('user_group')) {
      data['role'] = data.user_group;
    }
    merge(data, profile);
    return data;
  }
});
