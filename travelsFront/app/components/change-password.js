import Ember from 'ember';
import validate from 'ember-gen/validate';
import fetch from "ember-network/fetch";
import ENV from 'travel/config/environment';
import {validateConfirmation} from 'ember-changeset-validations/validators';

const {
  computed,
  get, set, inject, getOwner
} = Ember;

const PasswordModel = Ember.Object.extend({
  session: inject.service('session'),
  save() {
    let {new_password, re_new_password, current_password} = this.getProperties('new_password', 're_new_password', 'current_password');

    let url = ENV.APP.backend_host + '/auth/password/';
    let token = get(this, 'session.session.authenticated.auth_token');
    set(this, 'errors', []);

    return fetch(url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': `Token ${token}`
      },
      body: JSON.stringify({new_password, re_new_password, current_password})
    }).then((resp) => {
      if (200 <= resp.status && 300 > resp.status) {
        this.setProperties({new_password: '', re_new_password: '', current_password: ''});
        return this;
      }
      return resp.json().then((json) => {
        if (!json.detail) {
          let errors = [];
          Object.keys(json).forEach((key) => {
            errors.push({attribute: key, message: json[key]});
          })
          set(this, 'errors', errors);
          throw json;
        } else {
          let err = new Error(resp.statusText)
          err.detail = json.detail;
          throw err;
        }
      })
    })
  }
});

export default Ember.Component.extend({
  tagName: '',

  passwordModel: computed(function() {
    console.log("PasswordModel", PasswordModel.toString());
    return PasswordModel.create({container: getOwner(this)});
  }),

  modelMeta: {
    fields: [
      ['current_password', {
        type: 'string',
        formAttrs: { type: 'password' },
        validators: [validate.presence(true)]
      }],
      ['new_password', {
        type: 'string',
        formAttrs: { type: 'password' },
        validators: [validate.length({min: 6})]
      }],
      ['re_new_password', {
        type: 'string',
        formAttrs: { type: 'password' },
        validators: [validateConfirmation({ on: 'new_password' })]
      }]
    ]
  },

  cancel() {},

  actions: {
    onSubmit() { this.cancel(); } // close overlay
  }
})

