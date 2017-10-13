import Ember from 'ember';
import ApimasAuthenticator from 'ember-gen-apimas/authenticators/apimas';

const {
  merge
} = Ember;

export default ApimasAuthenticator.extend({
  profilePath: '/auth/me/detailed',
  processProfileData(data, profile) {
    merge(data, profile);
    return data;
  }
});
