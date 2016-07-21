import Ember from 'ember';

export function toDate(value) {
  var m = moment.utc(value[0]);
  return m.isValid() ? m.format("DD-MM-YYYY"): null;
}

export default Ember.Helper.helper(toDate);
