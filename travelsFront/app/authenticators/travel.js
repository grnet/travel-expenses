import ApimasAuthenticator from 'ember-gen-apimas/authenticators/apimas';

export default ApimasAuthenticator.extend({
  profilePath: '/auth/me/detailed',
  processProfileData(user) {
    if (!user.role) { user.role = 'USER'; }
    return user;
  }
});
