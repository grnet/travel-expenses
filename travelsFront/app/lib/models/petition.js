import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travels-front/config/environment'; 

const CHOICES = ENV.APP.resource_choices;

export var Petition = DS.Model.extend({
  first_name: DS.attr({attrs: {readonly: true}}),
  last_name: DS.attr(),
  specialty: DS.attr({'label': 'Specialty', 'choices': CHOICES.SPECIALTY}),
  kind: DS.attr({'choices': CHOICES.KIND}),
  tax_reg_num: DS.attr({'label': 'VAT'}),
  tax_office: DS.belongsTo('tax-office'),
  iban: DS.attr(),
  user_category: DS.attr({'label': 'User Category', 'choices': CHOICES.USER_CATEGORY}),
  user: DS.belongsTo('profile'),
  dse: DS.attr(),
  project: DS.belongsTo('project'),
  reason: DS.attr(),
  movement_category: DS.attr({attrs: {readonly: true}}),
  departure_point: DS.attr({'label': 'Depart from', 'choices': CHOICES.DEPARTURE_POINT}),
  arrival_point: DS.attr({'label': 'Arrive at', 'choices': CHOICES.ARRIVAL_POINT}),
  task_start_date: DS.attr({
    attrs: {
      type: 'datetime-local'
    },
    label: 'Task starts at'
  }),
  task_end_date: DS.attr({
    attrs: {
      type: 'datetime-local'
    },
    label: 'Task ends at'
  }),
  depart_date: DS.attr({
    attrs: {
      type: 'datetime-local'
    },
    label: 'Depart at'
  }),
  return_date: DS.attr({
    attrs: {
      type: 'datetime-local'
    },
    label: 'Return at'
  }),
  travel_info: DS.hasMany('travel-info'),
  
  status: DS.attr(),
  petition_id: Ember.computed('id', function(){
    // return just the status id
    return _.last(this.get('id').replace(/\/$/, '').split('/'));
  }),
  mean_of_transport: DS.attr({'label': 'Mean of Transport', 'choices': CHOICES.TRANSPORTATION}),
  transportation: DS.attr(),
  accommodation: DS.attr({'label': 'Mean of Transport', 'choices': CHOICES.ACCOMMODATION}),
  registration_cost: DS.attr(),
  additional_expenses: DS.attr(),
  meals: DS.attr({'label': 'Meals', 'choices': CHOICES.FEEDING}),
  non_grnet_quota: DS.attr(),
  user_recommendation: DS.attr()
});


    
       

