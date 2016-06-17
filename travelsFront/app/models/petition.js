import Ember from 'ember';
import DS from 'ember-data';
import {validator, buildValidations} from 'ember-cp-validations';

var Validations=buildValidations({

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
	user_category: DS.belongsTo('category'),
	taskStartDate: DS.attr(),
	taskEndDate: DS.attr(),
	depart_date: DS.attr(),
	return_date: DS.attr(),
	creationDate: DS.attr(),
	updateDate: DS.attr(),
	departurePoint: DS.belongsTo('city'),
	arrivalPoint: DS.belongsTo('city'),
	transportation: DS.belongsTo('transportation'),
	movementCategory: DS.belongsTo('movement-category'),
	project: DS.belongsTo('project'),
	reason: DS.attr(),
	recTransport: DS.attr(),
	recAccomondation: DS.attr(),
	recCostParticipation: DS.attr(),
	additional_expenses_sum: DS.attr(),
	//additional_expenses_initial: DS.attr(),
	//additional_expenses_initial_description: DS.attr(),
	status: DS.belongsTo('petition-status'),
	overnights_num: DS.attr(),
	overnights_num_proposed: DS.attr(),
	overnight_cost: DS.attr(),
	max_overnight_cost: DS.attr(),
	overnights_sum_cost: DS.attr(), 
	transport_days: DS.attr(),
	transport_days_proposed: DS.attr(),
	task_duration: DS.attr(),
	same_day_return_task: DS.attr(),
	compensation_level: DS.attr(),
	compensation_days: DS.attr(),
	compensation_days_proposed: DS.attr(),
	max_compensation: DS.attr(),
	compensation_final: DS.attr(),
	advanced_info: DS.belongsTo('advanced-petition'),
	trip_days_before: DS.attr(),
	trip_days_after: DS.attr(),
	total_cost: DS.attr()

});
