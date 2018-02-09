import DS from 'ember-data';
import moment from 'moment';

const DATE_FORMAT = "YYYY-MM-DDTHH:mm";

export default DS.Transform.extend({
  deserialize(serialized) {
    return serialized ? moment(serialized).toDate() : null;
  },

  serialize(deserialized) {
    return deserialized ? moment(deserialized).format(DATE_FORMAT) : null;
  }
});
