import DS from 'ember-data';

export default DS.Model.extend({
	name: DS.attr(),
	surname: DS.attr(),
	iban: DS.attr(),
	specialtyID: DS.belongsTo('specialty'),
	kind: DS.belongsTo('kind'),
	taxRegNum: DS.attr(),
	taxOffice: DS.belongsTo('tax-office'),
	taskStartDate: DS.attr(),
	taskEndDate: DS.attr(),
	departurePoint: DS.belongsTo('departure-point'),
	arrivalPoint: DS.belongsTo('arrival-point'),
	transportation: DS.belongsTo('transportation'),
	movementCategory: DS.belongsTo('movement-category'),
	project: DS.belongsTo('project'),
	reason: DS.attr(),
	recTransport: DS.attr(),
 	recAccomondation: DS.attr(),
 	recCostParticipation: DS.attr(),
 	petitionStatus: DS.belongsTo('petition-status')
});
