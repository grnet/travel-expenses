import ApimasAuthenticator from 'ember-gen-apimas/authenticators/apimas';

export default ApimasAuthenticator.extend({
  processProfileData(user) {
    if (!user.role) { user.role = 'USER'; }
    return user;
  }
});
