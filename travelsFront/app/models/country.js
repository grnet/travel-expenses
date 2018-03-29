import DS from 'ember-data';

export default DS.Model.extend({
  __api__: {
    path: 'countries',
  },
  name: DS.attr(),
  category: DS.attr(),
  currency: DS.attr(),
  url: DS.attr(),
});
