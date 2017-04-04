import gen from 'ember-gen/lib/gen';
import AuthGen from 'ember-gen/lib/auth';

const {
  get, computed
} = Ember;

export default AuthGen.extend({
  login: {
    config: {
      authenticator: 'travel'
    }
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
        fields: ['first_name', 'last_name', 'iban', 'specialty', 'kind', 'tax_reg_num', 'tax_office', 'user_category'],
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
