import Ember from 'ember';
import ENV from 'travel/config/environment';
import moment from 'moment';
import { field } from 'ember-gen';

const {
  get,
  computed,
  assign,
} = Ember;

const DATE_FORMAT = ENV.APP.date_format,
    DATE_TIME_FORMAT = ENV.APP.date_time_format;

function computeDateFormat(key) {
  return computed(key, function() {
    let date = get(this, key)

    return date ? moment(date).format(DATE_FORMAT) : '-';
  });
};

function computeDateTimeFormat(key) {
  return computed(key, function() {
    let date = get(this, key)

    return date ? moment(date).format(DATE_TIME_FORMAT) : '-';
  });
};

function fileField(key, path, kind, attrs, formAttrs) {
  return field(key, assign({}, {
    type: 'file',
    formComponent: 'travel-file-field',
    displayComponent: 'travel-file-field',
    displayAttrs: assign({ hideLabel: true }, { path, kind }, formAttrs || {}),
    sortBy: 'filename',
    formAttrs: assign({}, { path, kind }, formAttrs || {}),
  }, attrs || {}));
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookie = document.cookie;
    var csrftokenPosition = cookie.indexOf('csrftoken');
    cookieValue = decodeURIComponent(cookie.substring(csrftokenPosition + name.length + 1));
  }
  return cookieValue;
}

export { computeDateFormat, computeDateTimeFormat, fileField, getCookie };
