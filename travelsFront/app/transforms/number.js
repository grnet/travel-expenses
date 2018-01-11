import DS from 'ember-data';

export default DS.Transform.extend({
//sent data
  serialize: function(value) {
    if (typeof value === "string") {
      return value.replace(",", ".");
    }
    return value;
  },
//receive data
  deserialize: function(value) {
    if (typeof value === "number") {
      return value.toString().replace(".", ",");
    }
    return value;
  }
});
