import Ember from 'ember';
import fetch from "ember-network/fetch";
import ENV from 'travel/config/environment';

const {
  computed,
  get, set, inject, getOwner
} = Ember;

const PasswordModel = Ember.Object.extend({
  save() {
    let {new_password, re_new_password} = this.getProperties('new_password', 're_new_password');
    let [uid, token] = (this.get('token') || '').split('|');
    let url = ENV.APP.backend_host + '/auth/password/reset/confirm/';
    set(this, 'errors', []);

    return fetch(url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({new_password, re_new_password, uid, token})
    }).then((resp) => {
      if (200 <= resp.status && 300 > resp.status) {
        this.setProperties({new_password: '', re_new_password: ''});
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

  visiblePopup: true,

  model: computed(function() {
    return PasswordModel.create({container: getOwner(this), token: this.get('token')})
  }),

  modelMeta: {
    fields: [
      ['new_password', {type: 'string', required: true, formAttrs: { type: 'password' }}],
      ['re_new_password', {type: 'string', required: true, formAttrs: { type: 'password' }}],
    ]
  },

  actions: {
    onSubmit() { set(this, 'visiblePopup', false); } // close overlay
  }
})

