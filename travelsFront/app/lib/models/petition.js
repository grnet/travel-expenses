import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travels-front/config/environment'; 

const CHOICES = ENV.APP.resource_choices;

export var Petition = DS.Model.extend({
  // profile fields
  first_name: DS.attr({attrs: {disabled: true, required: true}}),
  last_name: DS.attr({attrs: {disabled: true, required: true}}),
  specialty: DS.attr({'label': 'Specialty', 'choices': CHOICES.SPECIALTY, attrs: {disabled: true}}),
  kind: DS.attr({'choices': CHOICES.KIND, attrs: {disabled: true}}),
  tax_reg_num: DS.attr({attrs: {disabled: true}, label: 'VAT'}),
  tax_office: DS.belongsTo('tax-office', {attrs: {disabled: true}}),
  iban: DS.attr({attrs: {disabled: true}}),
  category: DS.attr({'label': 'User Category', 'choices': CHOICES.USER_CATEGORY, attrs: {disabled: true}}),


  user: DS.belongsTo('profile'),
  dse: DS.attr('string', {attrs: {disabled: true, required: true}}),
  project: DS.belongsTo('project', {attrs: {labelKey: "full_label", required: true}}),
  //project: DS.attr(),
  reason: DS.attr({attrs: {required: true, textarea: true}}),
  movement_category: DS.attr({choices: CHOICES.MOVEMENT_CATEGORIES, attrs: {disabled: true}}),
  departure_point: DS.belongsTo('city', {attrs: {required: true}}),
  arrival_point: DS.belongsTo('city', {attrs: {required: true}}),
  country_category: DS.attr('string', {attrs: {disabled: true}}),
  task_start_date: DS.attr('date', {
    attrs: {
      time: true,
      required: true    
    },
    label: 'Task starts at'
  }),
  task_end_date: DS.attr('date', {
    attrs: {
      time: true,
      required: true 
    },
    label: 'Task ends at'
  }),  
  status: DS.attr(),
  petition_id: Ember.computed('id', function(){
    // return just the status id
    return _.last(this.get('id').replace(/\/$/, '').split('/'));
  }),
  registration_cost: DS.attr({attrs: {required: true}}),
  additional_expenses: DS.attr({attrs: {required: true}}),
  non_grnet_quota: DS.attr({attrs: {required: true}}),
  user_recommendation: DS.attr({attrs:{textarea: true}}),

  //Travel_info DATA
  travel_info: DS.attr(),
  // depart_date: DS.attr('date', {
  //   attrs: {
  //     time: true
  //   },
  //   label: 'Depart at'
  // }),
  // return_date: DS.attr('date', {
  //   attrs: {
  //     time: true
  //   },
  //   label: 'Return at'
  // }),
  // meals: DS.attr({'label': 'Meals', 'choices': CHOICES.MEALS}),
  // means_of_transport: DS.attr({'label': 'Means of Transport', 'choices': CHOICES.TRANSPORTATION}),
  // transportation: DS.attr(),
  // accommodation: DS.attr(),
  //
  observeDeparturePoint: Ember.observer('arrival_point', function() {
    this.get('arrival_point').then((city) => {
      if (!city) {
        this.set('country_category', null);
        this.set('movement_category', null);
      } else {
        this.set('country_category', city.get('country.category'));
        if (city.get('country.name') == 'ΕΛΛΑΔΑ') {
          this.set('movement_category', '1');
        } else {
          this.set('movement_category', '2');
        }
      }
    })
  })
});
