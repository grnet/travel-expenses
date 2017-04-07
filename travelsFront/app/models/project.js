import DS from 'ember-data';

export default DS.Model.extend({
  __api__: {
    ns: '/'
  },

	name: DS.attr(),
	accountingCode: DS.attr(),
	manager: DS.attr(),
	url: DS.attr()
});
