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
  __form__: {
    layout: [33],
    layoutMap: {"reason": 100},
    fieldsets: [
      {
        'label': 'Profile',
        'fields': ['name', 'surname', 'iban', 'specialtyID', 
          'kind', 'taxRegNum', 'taxOffice', 'user_category']
      },
      {
        'label': 'Dates',
        'fields': ['taskStartDate', 'taskEndDate', 
          'depart_date', 'return_date', 'creationDate', 'updateDate']
      },
      {
        'label': 'Transportation',
        'fields': [
          'departurePoint', 'arrivalPoint', 'transportation',
          'movementCategory'
        ]
      },
      {
        'label': 'Project',
        'fields': [
          'project', 'reason', 'recTransport', 'recAccomondation',
          'recCostParticipation'
        ]
      },
      {
        'label': 'Expenses',
        'fields': [
          'additional_expenses_sum', 'additional_expenses_initial',
          'additional_expenses_initial_description',
          'status', 'overnights_num', 'overnights_num_proposed',
          'overnight_cost', 'max_overnight_cost', 'overnights_sum_cost'
        ]
      },
      {
        'label': 'Duration',
        'fields': [
          'transport_days', 'transport_days_proposed', 'task_duration',
          'same_day_return_task', 'compensation_level', 'compensation_days_proposed',
          'max_compensation', 'compensation_final', 'advanced_info', 'trip_days_before',
          'trip_days_after', 'total_cost'
        ]
      }
    ]
  }, 

	name: DS.attr({
    hint: 'Provide your name'
  }),
	surname: DS.attr(),
	iban: DS.attr({
    hint: new Ember.Handlebars.SafeString('This should be your IBAN number. See <a href="lla">here</a> for more details.')
  }),
	specialtyID: DS.belongsTo('specialty'),
	kind: DS.belongsTo('kind'),
	taxRegNum: DS.attr(),
	taxOffice: DS.belongsTo('tax-office'),
	user_category: DS.belongsTo('category'),
	taskStartDate: DS.attr(),
	taskEndDate: DS.attr(),
	depart_date: DS.attr(),
	return_date: DS.attr({
    fieldAttrs: {
      type: 'datetime-local'
    }
  }),
	creationDate: DS.attr({
    fieldAttrs: {
      type: 'date'
    }
  }),
	updateDate: DS.attr(),
	departurePoint: DS.belongsTo('city'),
	arrivalPoint: DS.belongsTo('city'),
	transportation: DS.belongsTo('transportation'),
	movementCategory: DS.belongsTo('movement-category'),
	project: DS.belongsTo('project'),
	reason: DS.attr({fieldAttrs: {
    textarea: true,
    rows: 20
  }}),
	recTransport: DS.attr(),
	recAccomondation: DS.attr(),
	recCostParticipation: DS.attr(),
	additional_expenses_sum: DS.attr(),
	additional_expenses_initial: DS.attr(),
	additional_expenses_initial_description: DS.attr(),
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
