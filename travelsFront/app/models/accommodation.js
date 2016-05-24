import DS from 'ember-data';

export default DS.Model.extend({
	hotel: DS.attr(),
	hotelPrice: DS.attr(),
	url: DS.attr()

});
