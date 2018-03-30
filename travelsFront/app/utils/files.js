import DS from 'ember-data';
import Ember from 'ember';
import fetch from 'ember-network/fetch';

const {
  get,
  RSVP: { Promise },
} = Ember;

function uploadFile(file, url, token, file_data_key = 'file_upload') {
  let data = new FormData();

  data.append(file_data_key, file);

  return fetch(url, {
    method: 'PUT',
    headers: {
      'Accept': 'application/json',
      'Authorization': `Token ${token}`,
    },
    body: data,
  }).then((resp) => {
    if (resp.status < 200 || resp.status > 299) {
      return resp.json().then((jresp) => {
        throw jresp;
      })
    } else {
      return file;
    }
  })
}

function uploadFiles(files, url, token) {
  // TODO: support for multiple uploads?
}

// changeset.<field> value can be either a model or a model promise
function getFile(content, key) {
  let value = get(content, `model.changeset.${key}`)

  if (value && (value instanceof DS.Model)) { return value; }

  return value && value.content;
}

export { uploadFile, uploadFiles, getFile };