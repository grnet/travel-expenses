import DS from 'ember-data';

export default DS.Model.extend({
	taskStartDate: DS.attr(),
	taskEndDate: DS.attr(),
	taskStartTime: DS.attr(),
	taskEndTime: DS.attr(),
	departurePoint: DS.belongsTo('departure-point'),
	arrivalPoint: DS.belongsTo('arrival-point'),
	transportation: DS.belongsTo('transportation'),
	movementCategory: DS.belongsTo('movement-category'),
	project: DS.belongsTo('project'),
	reason: DS.attr(),
	recTransport: DS.attr(),
 	recAccomondation: DS.attr(),
 	recCostParticipation: DS.attr()
});
