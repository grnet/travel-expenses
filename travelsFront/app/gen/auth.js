import gen from 'ember-gen/lib/gen';
import AuthGen from 'ember-gen/lib/auth';
import routes from 'ember-gen/lib/routes';

const {
  get, computed
} = Ember;

export default AuthGen.extend({
  login: {
    config: {
      authenticator: 'token'
    }
  },

  profile: {
  	
    modelName: 'profile',
    menu: { display: true, icon: 'perm_identity',},

    getModel() {
      return get(this, 'store').findRecord('profile', 'me');
    }
  	
  }
})

