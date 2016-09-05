import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travels-front/config/environment'; 

const CHOICES = ENV.APP.resource_choices,
      CURRENCY = [[ENV.default_currency, ENV.default_currency]];

export var Petition = DS.Model.extend({
  // profile fields
  first_name: DS.attr({attrs: {disabled: true, required: true}}),
  last_name: DS.attr({attrs: {disabled: true, required: true}}),
  specialty: DS.attr({'choices': CHOICES.SPECIALTY, attrs: {disabled: true}}),
  kind: DS.attr({'choices': CHOICES.KIND, attrs: {disabled: true}}),
  tax_reg_num: DS.attr({attrs: {disabled: true}}),
  tax_office: DS.belongsTo('tax-office', {attrs: {disabled: true}}),
  iban: DS.attr({attrs: {disabled: true}}),
  user_category: DS.attr({'choices': CHOICES.USER_CATEGORY, attrs: {disabled: true}}),
  //petition fields
  user: DS.belongsTo('profile'),
  dse: DS.attr('string', {attrs: {disabled: true, required: true}}),
  project: DS.belongsTo('project', {attrs: {labelKey: "full_label", required: true}}),
  reason: DS.attr({attrs: {required: true, textarea: true}}),
  movement_category: DS.attr({choices: CHOICES.MOVEMENT_CATEGORIES, attrs: {disabled: true}}),
  country_category: DS.attr('string', {attrs: {disabled: true}}),
  created: DS.attr('date', {attrs: {time: true, required: true}}),
  updated: DS.attr('date', {attrs: {time: true, required: true}}),
  task_start_date: DS.attr('date', {
    attrs: {
      time: true,
      required: true
    }}),
  task_end_date: DS.attr('date', {
    attrs: {
      time: true,
      required: true
    }}),
  status: DS.attr(),
  petition_id: Ember.computed('id', function(){
    // return just the status id
    return _.last(this.get('id').replace(/\/$/, '').split('/'));
  }),
  participation_local_cost: DS.attr({attrs: {required: true}}),
  participation_local_currency: DS.attr({'choices': CURRENCY, 'component': 'petition-currency'}),
  additional_expenses_initial: DS.attr({attrs: {required: true}}),
  additional_expenses_initial_description: DS.attr({attrs:{textarea: true}}),
  user_recommendation: DS.attr({attrs:{textarea: true}}),

  //Travel_info DATA
  travel_info: DS.attr(),
  departure_point: DS.belongsTo('city', {attrs: {required: true, autocomplete: true, labelKey: 'labelWithCountry'}}),
  arrival_point: DS.belongsTo('city', {attrs: {required: true, autocomplete: true, labelKey: 'labelWithCountry'}}),
  depart_date: DS.attr('date', {
    attrs: {
      time: true
    }}),
  return_date: DS.attr('date', {
    attrs: {
      time: true
    }}),
  meals: DS.attr({'choices': CHOICES.MEALS}),
  means_of_transport: DS.attr({'choices': CHOICES.TRANSPORTATION}),
  transportation_cost: DS.attr(),
  accommodation_local_cost: DS.attr(),
  accommodation_local_currency: DS.attr({'choices': CURRENCY, 'component': 'petition-currency'}),
  //set movement/country category value
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
