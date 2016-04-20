import DS from 'ember-data';

export default DS.Model.extend({
	travelID: DS.attr(),
	taskStartDate: DS.attr(),
	taskEndDate: DS.attr(),
	taskStartTime: DS.attr(),
	taskEndTime: DS.attr(),
	departurePoint: DS.attr(),
	arrivalPoint: DS.attr(),
	meanOfTransport: DS.attr(),
	categoryOfTransport: DS.attr(),
	project: DS.attr(),
	reasonOfTransport: DS.attr(),
	recMeanOfTransport: DS.attr(),
 	recHotel: DS.attr(),
 	recCostParticipation: DS.attr()
});
