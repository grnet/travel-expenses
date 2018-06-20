import Ember from 'ember';
import AuthGen from 'ember-gen/lib/auth';
import { Register, resetHash } from '../lib/register';
import PROFILE from '../utils/common/profile';
import { applicationActions } from '../utils/common/actions';
import ENV from 'travel/config/environment';
import fetch from "ember-network/fetch";

const {
  get,
} = Ember;

function extractError(loc) {
  return loc.hash && loc.hash.split("error=")[1];
};

function extractReset(loc) {
  return loc.hash && loc.hash.split("reset=")[1];
};

function extractActivate(loc) {
  return loc.hash && loc.hash.split("activate=")[1];
};

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
    menu: {
      icon: 'fingerprint',
    },
    config: {
      authenticator: 'travel',
    },
    templateName: 'travel-login',
    routeMixins: [{
      handleActivate(activate) {
        let [uid, token] = activate.split("|");
        resetHash(window);
        if (uid && token) {
          let url = ENV.APP.backend_host + '/auth/activate/';
          let data = {uid, token};
          return fetch(url, {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
          }).then((resp) => {
            let err, msg;
            if (resp.status === 200) {
              msg = 'user.email_verification.success';
            } else {
              err = 'user.email_verification.error';
              resp.json().then((json) => {
                if (!json.detail) { return; }
                this.get('messageService').setError(json.detail);
              });
              resetHash(window, "error=user.email_verification.error");
            }
            if (msg) { this.get('messageService').setSuccess(msg); }
            if (err) { this.get('messageService').setError(err); }
          });
        }
      },

      beforeModel(transition) {
        let activate = extractActivate(window.location);
        if (activate) {
          return this.handleActivate(decodeURI(activate)).finally(() => {
            return this.transitionTo('index');
          });
        }
        return this._super(transition);
      },

      setupController(controller, model) {
        this._super(controller, model);

        let error = extractError(window.location);
        error = decodeURI(error);

        let reset = extractReset(window.location);
        if (reset) { controller.set('resetToken', decodeURI(reset)); }
      },
     }]
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

