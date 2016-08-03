import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travels-front/config/environment';

const CHOICES = ENV.APP.resource_choices;

export default DS.Model.extend({
  __api__: {
    ns: 'petition'
  },
  url: DS.attr(),
  departure_point: DS.belongsTo('city', {attrs: {required: true}}),
  arrival_point: DS.belongsTo('city', {attrs: {required: true}}),
  depart_date: DS.attr('date', {
    attrs: {
      time: true
    },
    label: 'Depart at'
  }),
  return_date: DS.attr('date', {
    attrs: {
      time: true
    },
    label: 'Return at'
  }),
  meals: DS.attr({'label': 'Meals', 'choices': CHOICES.MEALS}),
  means_of_transport: DS.attr({'label': 'Means of Transport', 'choices': CHOICES.TRANSPORTATION}),
  // transport_days_manual: DS.attr(),
  // transport_days_proposed: DS.attr(),
  // overnights_num_manual: DS.attr(),
  // compensation_days_manual: DS.attr(),
  // compensation_days_proposed: DS.attr(),
  accommodation_local_cost: DS.attr(),
  // accommodation_cost: DS.attr(),
  // accommodation_default_currency: DS.attr(),
  accommodation_local_currency: DS.attr({'label': 'Currency', 'choices': CHOICES.CURRENCIES}),
  // accommodation_payment_way: DS.attr(),
  // accommodation_payment_description: DS.attr(),
  transportation_cost: DS.attr(),
  // transportation_default_currency: DS.attr(),
  // transportation_payment_way: DS.attr(),
  // transportation_payment_description: DS.attr(),
  //overnights_num_manualQ DS.attr(),
  // overnight_cost: DS.attr(),
  // compensation_level: DS.attr(),
  // same_day_return_task: DS.attr(),
});
