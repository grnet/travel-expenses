import Ember from 'ember';
import fetch from "ember-network/fetch";
import ENV from 'travel/config/environment';

const {
  computed,
  get, set, inject, getOwner
} = Ember;

const PasswordModel = Ember.Object.extend({
  save() {
    let email = this.get('email');

    let url = ENV.APP.backend_host + '/auth/password/reset/';
    set(this, 'errors', []);

    return fetch(url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({email})
    }).then((resp) => {
      if (200 <= resp.status && 300 > resp.status) {
        this.setProperties({email: ''});
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

  formModel: computed(function() {
    return PasswordModel.create({container: getOwner(this)})
  }),

  modelMeta: {
    fields: [
      ['email', {type: 'string', required: true, formAttrs: { type: 'email' }}],
    ]
  },

  cancel() {},

  actions: {
    onSubmit() { this.cancel(); } // close overlay
  }
})

