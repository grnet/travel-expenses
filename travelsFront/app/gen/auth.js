import Ember from 'ember';
import AuthGen from 'ember-gen/lib/auth';
import { Register } from '../lib/register';
import PROFILE from '../utils/common/profile';

const {
  get,
} = Ember;

export default AuthGen.extend({
  order: 100,
  login: {
    page: {
      title: 'login.label',
    },
    config: {
      authenticator: 'travel',
    },
  },

  gens: {
    register: Register,
  },

  profile: {
    modelName: 'profile',
    page: {
      title: 'profile.menu_label',
    },
    menu: {
      display: true,
      icon: 'portrait',
      label: 'profile.tab',
    },
    fieldsets: PROFILE.FS_EDIT,
    validators: PROFILE.FS_VALIDATORS,

    getModel() {
      return get(this, 'store').findRecord('profile', 'me');
    },
  },
})
