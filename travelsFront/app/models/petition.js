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

export default DS.Model.extend(Validations, {
  __ui__: {
    "user": {
      layoutMap: {"reason": 100},
      fieldsets: [
        {
          'label': 'Profile',
          'fields': ['name', 'surname', 'specialtyID', 
          'kind', 'taxRegNum', 'taxOffice', 'iban', 'user_category']
        },
        {
          'label': 'Travel Data',
          'fields': ['dse', 'project', 'reason', 'movementCategory', 'departurePoint', 'arrivalPoint',
          'taskStartDate', 'taskEndDate', 'depart_date', 'return_date', 'transportation', 'flight',
          'accomondation', 'recCostParticipation', 'additional_expenses_initial', 'feeding', 'non_grnet_quota']
        },
      ],
      layout: {
        flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
      }
    },
    "secretary": {
      layoutMap: {"reason": 100},
      fieldsets: [
        {
          'label': 'Profile',
          'fields': ['name', 'surname', 'specialtyID', 
          'kind', 'taxRegNum', 'taxOffice', 'iban', 'user_category']
        },
        {
          'label': 'Travel Data',
          'fields': ['dse', 'project', 'reason', 'movementCategory', 'departurePoint', 'arrivalPoint',
          'taskStartDate', 'taskEndDate', 'depart_date', 'return_date', 'transportation', 'flight',
          'accomondation', 'recCostParticipation', 'additional_expenses_initial', 'feeding', 'non_grnet_quota']
        },
        {
          'label': 'Secretary Data',
          'fields': ['movement_num', 'expenditure_date_protocol',
          'expenditure_protocol', 'movement_date_protocol', 'movement_protocol', 'trip_days_before']
        },
        {
          'label': 'Computed Data',
          'fields': ['transport_days_manual', 'transport_days_proposed', 'overnights_num_manual',
          'overnights_num_proposed', 'compensation_days_manual', 'compensation_days_proposed', 'same_day_return_task', 
          'trip_days_before', 'trip_days_after', 'overnights_sum_cost', 'compensation_level', 'compensation_final', 'total_cost']
        },
      ],
      layout: {
        flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
      }
    }

  },

  //profile
	name: DS.attr({
    hint: 'Provide your name'
  }),
	surname: DS.attr(),
	iban: DS.attr({'label': 'IBAN'}, {
    hint: new Ember.Handlebars.SafeString('This should be your IBAN number. See <a href="lla">here</a> for more details.')
  }),
	specialtyID: DS.belongsTo('specialty', {'label': 'Specialty'}),
	kind: DS.belongsTo('kind'),
	taxRegNum: DS.attr({'label': 'VAT'}),
	taxOffice: DS.belongsTo('tax-office'),
	user_category: DS.belongsTo('category'),

  //user data
  dse: DS.attr(),
  project: DS.belongsTo('project'),
  reason: DS.attr({'label': 'Movement Justification'}, {attrs: {
    textarea: true,
    rows: 20
  }}),
  movementCategory: DS.belongsTo('movement-category'),
  departurePoint: DS.belongsTo('city'),
  arrivalPoint: DS.belongsTo('city'),
	taskStartDate: DS.attr({
    attrs: {
      type: 'datetime-local'
    },
    label: 'Task starts at'
  }),
	taskEndDate: DS.attr({
    attrs: {
      type: 'datetime-local'
    },
    label: 'Task ends at'
  }),
	depart_date: DS.attr({
    attrs: {
      type: 'datetime-local'
    }
  }),
	return_date: DS.attr({
    attrs: {
      type: 'datetime-local'
    }
  }),
  transportation: DS.belongsTo('transportation'),
  flight: DS.belongsTo('flight', {component:'paper-input'}),
  accomondation: DS.belongsTo('accommondation'),
  recCostParticipation: DS.attr({'label': 'Registration Cost'}),
  additional_expenses_initial: DS.attr({'label': 'Additional Costs'}),
  feeding: DS.belongsTo('feeding'),
  non_grnet_quota: DS.attr(),
	creationDate: DS.attr({
    attrs: {
      type: 'datetime-local'
    }
  }),
	updateDate: DS.attr({
    attrs: {
      type: 'datetime-local'
    }
  }),
	additional_expenses_sum: DS.attr(),
	additional_expenses_initial_description: DS.attr(),
	status: DS.belongsTo('petition-status'),
  //recTransport: DS.attr(),
  //recAccomondation: DS.attr(),
	
  //secretary data
  movement_num: DS.attr(),
  expenditure_protocol: DS.attr(), 
  expenditure_date_protocol: DS.attr(),
  movement_protocol: DS.attr(),
  movement_date_protocol: DS.attr(),
  compensation_petition_protocol: DS.attr(),
  compensation_petition_date: DS.attr(),
  compensation_decision_protocol: DS.attr(),
  compensation_decision_date: DS.attr(),
  trip_days_before: DS.attr(),
  trip_days_after: DS.attr(),
  grnet_quota: DS.attr(),
  compensation: DS.belongsTo('compensation-categories'),
  transport_days: DS.attr(),
  transport_days_manual: DS.attr('number'),
  transport_days_proposed: DS.attr(),
  overnights_num: DS.attr(),
  overnights_num_manual: DS.attr('number'),
  overnights_num_proposed: DS.attr(),
  compensation_days: DS.attr(),
  compensation_days_manual: DS.attr('number'),
  compensation_days_proposed: DS.attr(),
  overnight_cost: DS.attr(),
  max_overnight_cost: DS.attr(),
  overnights_sum_cost: DS.attr(), 
  task_duration: DS.attr(),
  same_day_return_task: DS.attr(),
  compensation_level: DS.attr(),
  max_compensation: DS.attr(),
  compensation_final: DS.attr(),
  total_cost: DS.attr(),
  //advanced_info: DS.belongsTo('advanced-petition'),
});
