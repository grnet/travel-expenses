import DS from 'ember-data';

export default DS.Model.extend({
	name: DS.attr(),
	country: DS.belongsTo('country'),
	url: DS.attr()

});
