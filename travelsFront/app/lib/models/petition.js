import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travels-front/config/environment'; 

const CHOICES = ENV.APP.resource_choices;

export var Petition = DS.Model.extend({
  first_name: DS.attr({attrs: {readonly: true, required: true}}),
  last_name: DS.attr({attrs: {readonly: true, required: true}}),
  specialty: DS.attr({'label': 'Specialty', 'choices': CHOICES.SPECIALTY, 'required': true}),
  kind: DS.attr({'choices': CHOICES.KIND, 'required': true}),
  tax_reg_num: DS.attr({attrs: {required: true}, label: 'VAT'}),
  tax_office: DS.belongsTo('tax-office', {attrs: {required: true}}),
  iban: DS.attr({attrs: {required: true}}),
  user_category: DS.attr({'label': 'User Category', 'choices': CHOICES.USER_CATEGORY, 'readonly': true}),
  user: DS.belongsTo('profile'),
  dse: DS.attr('string', {attrs: {required: true}}),
  project: DS.belongsTo('project', {attrs: {required: true}}),
  reason: DS.attr({attrs: {required: true}}),
  movement_category: DS.attr({attrs: {readonly: true}}),
  departure_point: DS.belongsTo('city', {attrs: {required: true}}),
  arrival_point: DS.belongsTo('city', {attrs: {required: true}}),
  task_start_date: DS.attr({
    attrs: {
      type: 'datetime-local',
      required: true
    },
    label: 'Task starts at'
  }),
  task_end_date: DS.attr({
    attrs: {
      type: 'datetime-local',
      required: true
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
  means_of_transport: DS.attr({'label': 'Mean of Transport', 'choices': CHOICES.TRANSPORTATION}),
  transportation: DS.attr(),
  accommodation: DS.attr({'label': 'Mean of Transport', 'choices': CHOICES.ACCOMMODATION}),
  registration_cost: DS.attr({attrs: {required: true}}),
  additional_expenses: DS.attr({attrs: {required: true}}),
  meals: DS.attr({'label': 'Meals', 'choices': CHOICES.FEEDING}),
  non_grnet_quota: DS.attr({attrs: {required: true}}),
  user_recommendation: DS.attr()
});


    
       

