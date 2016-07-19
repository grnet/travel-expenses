import DS from 'ember-data';

export default DS.Model.extend({
  __api__: {
    ns: 'users_related'
  },
	name: DS.attr(),
	accountingCode: DS.attr(),
	url: DS.attr()
  
});
