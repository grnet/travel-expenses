import Ember from 'ember';
import gen from 'ember-gen/lib/gen';
import AuthGen from 'ember-gen/lib/auth';
import {Register} from '../lib/register';

const {
  get, computed
} = Ember;

export default AuthGen.extend({
  order: 100,
  login: {
    config: {
      authenticator: 'travel'
    }
  },

  gens: {
    register: Register
  },

  profile: {
    modelName: 'profile',
    menu: {
      display: true,
      icon: 'portrait',
      label: 'profile.tab',
    },
    fieldsets: [
      {
        label: 'my_account.label',
        fields: ['username', 'email'],
        layout: {
          flex: [50, 50]
        }
      },
      {
        label: 'personal_info.label',
        fields: ['first_name', 'last_name', 'specialty', 'kind', 'tax_reg_num', 'tax_office', 'iban', 'user_category'],
        layout: {
          flex: [50, 50, 50, 50, 50, 50, 50, 50]
        }
      }
    ],

    getModel() {
      return get(this, 'store').findRecord('profile', 'me');
    }
  }
})
