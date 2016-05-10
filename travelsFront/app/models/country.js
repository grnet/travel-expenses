import DS from 'ember-data';

export default DS.Model.extend({
	name: DS.attr(),
	category: DS.belongsTo('country-category'),
	url: DS.attr()

});
