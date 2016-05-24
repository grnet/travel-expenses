import DS from 'ember-data';

export default DS.Model.extend({
	flightName: DS.attr(),
	flightPrice: DS.attr(),
	url: DS.attr()

});
