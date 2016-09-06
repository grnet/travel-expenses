import DS from 'ember-data';

export default DS.DateTransform.extend({
  serialize(deserialized) {
    let value = this._super(deserialized);
    if (typeof value === "string") {
      return value.slice(0, 10);
    }
    return value;
  }
});
