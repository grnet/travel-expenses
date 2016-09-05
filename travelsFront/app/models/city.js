import DS from 'ember-data';

export default DS.Model.extend({
  __api__: {
    ns: 'resources'
  },

	name: DS.attr(),
	url: DS.attr(),
  country: DS.belongsTo('country'),
  labelWithCountry: Ember.computed('country', function() {
    return this.get('name') + ' [' + this.get('country.name') + ']';
  })
});
