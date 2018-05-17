import Ember from 'ember';
import AuthGen from 'ember-gen/lib/auth';
import { Register } from '../lib/register';
import PROFILE from '../utils/common/profile';
import { applicationActions } from '../utils/common/actions';

const {
  get,
} = Ember;

export default AuthGen.extend({
  order: 100,
  login: {
    extraActions: [
      {
        label: 'password.forgot',
        confirm: true,
        action: function() {},
        prompt: {
          title: 'password.forgot.title',
          contentComponent: 'forgot-password',
          noControls: true
        }
      }
    ],
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
    actions: ['change_password'],
    actionsMap: {
      'change_password': applicationActions.change_password
    },
    fieldsets: PROFILE.FS_EDIT,
    validators: PROFILE.FS_VALIDATORS,

    getModel() {
      return get(this, 'store').findRecord('profile', 'me');
    },
  },
})
