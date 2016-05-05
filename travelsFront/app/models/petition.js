import Ember from 'ember';
import DS from 'ember-data';
import {validator, buildValidations} from 'ember-cp-validations';

var Validations=buildValidations({
	//email: [
	//validator('presence', true),
	//validator('format', { type: 'email' })
	//],
	taxRegNum: validator('afm-validator'),
	iban: validator('iban-validator'),
	project: [
		validator('presence', true),
	]


});

export default DS.Model.extend(Validations,{
	name: DS.attr(),
	surname: DS.attr(),
	iban: DS.attr(),
	specialtyID: DS.belongsTo('specialty'),
	kind: DS.belongsTo('kind'),
	taxRegNum: DS.attr(),
	taxOffice: DS.belongsTo('tax-office'),
	taskStartDate: DS.attr(),
	taskEndDate: DS.attr(),
	creationDate: DS.attr(),
	updateDate: DS.attr(),
	departurePoint: DS.belongsTo('departure-point'),
	arrivalPoint: DS.belongsTo('arrival-point'),
	transportation: DS.belongsTo('transportation'),
	movementCategory: DS.belongsTo('movement-category'),
	project: DS.belongsTo('project'),
	reason: DS.attr(),
	recTransport: DS.attr(),
	recAccomondation: DS.attr(),
	recCostParticipation: DS.attr(),
	status: DS.belongsTo('petition-status')
});
