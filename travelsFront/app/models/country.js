import DS from 'ember-data';

export default DS.Model.extend({
  __api__: {
    ns: 'resources'
  },
	name: DS.attr(),
	category: DS.attr(),
	currency: DS.attr(),
	url: DS.attr()
});
