import DS from 'ember-data';

export default DS.Model.extend({
	travelID: DS.attr(),
	taskStartDate: DS.attr(),
	taskStartTime: DS.attr(),
	taskEndTime: DS.attr(),
	taskEndDate: DS.attr(),
	departurePoint: DS.attr(),
	arrivalPoint: DS.attr(),
	meanOfTransport: DS.attr(),
	categoryOfTransport: DS.attr(),
	project: DS.attr(),
	recMeanOfTransport: DS.attr(),
 	recHotel: DS.attr(),
 	recCostParticipation: DS.attr()
});
