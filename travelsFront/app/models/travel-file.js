import Ember from 'ember';
import DS from 'ember-data';
import fetch from 'ember-network/fetch';

const {
  get, set,
  computed,
  computed: { reads },
  inject
} = Ember;

export default DS.Model.extend({

  messages: inject.service('messages'),
  session: inject.service('session'),
  token: reads('session.session.authenticated.auth_token'),
  generatingLink: false,

  file_kind: DS.attr(),
  file_name: DS.attr(),
  owner: DS.attr(),
  source: DS.attr(),
  description: DS.attr(),
  updated_at: DS.attr('date'),

  filename: reads('file_name'),


  downloadURL: computed(function() {
    let modelName = this.constructor.modelName;
    let adapter = this.store.adapterFor(modelName);
    let url = adapter.urlForModel(this) + 'download/';
    return url;
  }),

  download() {
    let url = get(this, 'downloadURL');
    let token = get(this, 'token');

    set(this, 'generatingLink', true);
    return fetch(url, {
      method: 'HEAD',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Token ${token}`
      }
    }).then((resp) => {
      if (resp.status < 200 || resp.status > 299) {
        throw resp;
      }
      let url = resp.headers.get('x-file-location');
      return url;
    }).catch((err) => {
      // TODO: resolve error message
      get(this, 'messages').setError('download.error');
      throw err;
    }).finally(() => {
      set(this, 'generatingLink', false);
    });
  }
});
