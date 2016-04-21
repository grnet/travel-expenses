import DS from 'ember-data';

export default DS.Model.extend({
	travelID: DS.attr(),
	taskStartDate: DS.attr(),
	taskEndDate: DS.attr(),
	taskStartTime: DS.attr(),
	taskEndTime: DS.attr(),
	departure_point: DS.belongsTo('departurePoint'),
	arrival_point: DS.belongsTo('arrivalPoint'),
	transportation: DS.belongsTo('meanOfTransport'),
	movement_categories: DS.belongsTo('categoryOfTransport'),
	project: DS.belongsTo('project'),
	reasonOfTransport: DS.attr(),
	recMeanOfTransport: DS.attr(),
 	recHotel: DS.attr(),
 	recCostParticipation: DS.attr()
});
