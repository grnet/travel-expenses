import AuthGen from 'ember-gen/lib/auth';

export default AuthGen.extend({
  login: {
    config: {
      authenticator: 'token'
    }
  }
})
