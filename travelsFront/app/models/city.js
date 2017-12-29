import Ember from 'ember';
import DS from 'ember-data';

export default DS.Model.extend({
  __api__: {
    path: 'city'
  },
  name: DS.attr(),
  url: DS.attr(),
  country: DS.belongsTo('country'),
  timezone: DS.attr(),
  labelWithCountry: Ember.computed('country', function() {
    return `${this.get('name')} [${this.get('country.name')}]`
  })
});
