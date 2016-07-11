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
            'kind', 'taxRegNum', 'taxOffice','iban', 'user_category']
        },
        {
          'label': 'Travel Data',
          'fields': ['project', 'reason', 'departurePoint', 'arrivalPoint',
          'taskStartDate', 'taskEndDate', 'depart_date', 'return_date',
          'transportation', 'recCostParticipation', 'additional_expenses_initial']
        },
      ],
      layout: {
        flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
      }
    }
  },

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
	departurePoint: DS.belongsTo('city'),
	arrivalPoint: DS.belongsTo('city'),
	transportation: DS.belongsTo('transportation'),
	movementCategory: DS.belongsTo('movement-category'),
	project: DS.belongsTo('project'),
	reason: DS.attr({'label': 'Movement Justification'}, {attrs: {
    textarea: true,
    rows: 20
  }}),
	recTransport: DS.attr(),
	recAccomondation: DS.attr(),
	recCostParticipation: DS.attr({'label': 'Registration Cost'}),
	additional_expenses_sum: DS.attr(),
	additional_expenses_initial: DS.attr({'label': 'Additional Costs'}),
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
