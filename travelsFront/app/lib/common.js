import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travel/config/environment';
import moment from 'moment';

const {
  get,
  computed: { reads },
  computed,
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

export { computeDateFormat, computeDateTimeFormat };
