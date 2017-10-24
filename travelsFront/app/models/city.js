import DS from 'ember-data';

export default DS.Model.extend({
  __api__: {
    path: 'city'
  },
  name: DS.attr(),
  url: DS.attr(),
  country: DS.belongsTo('country'),
  timezone: DS.attr(),
});
