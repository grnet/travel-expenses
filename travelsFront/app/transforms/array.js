import DS from 'ember-data';

export default DS.Transform.extend({
  deserialize(value) {
    return (Ember.typeOf(value) == "array") ? value : [];
  },

  serialize(value) {
    var type = Ember.typeOf(value);
    
    if (type == 'array') {
      return value
    } else if (type == 'string') {
      return value.split(',').map(function (item) {
        return jQuery.trim(item);
      });
    } else {
      return [];
    }
  }
});
