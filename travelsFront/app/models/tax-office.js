import DS from 'ember-data';

export default DS.Model.extend({
  __api__: {
    ns: 'resources'
  },
	name:  DS.attr(),
	kindDescription:  DS.attr(),
	address:  DS.attr(),
	email:  DS.attr(),
	phone:  DS.attr(),
	url: DS.attr()
});
