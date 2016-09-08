import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travels-front/config/environment';

const CHOICES = ENV.APP.resource_choices;
      CURRENCY = [[ENV.default_currency, ENV.default_currency]];
      
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
  meals: DS.attr({'choices': CHOICES.MEALS}),
  means_of_transport: DS.attr({'choices': CHOICES.TRANSPORTATION}),
  transportation_cost: DS.attr(),
  accommodation_local_cost: DS.attr(),
  accommodation_local_currency: DS.attr({'choices': CHOICES.CURRENCIES}),
  transport_days_manual: DS.attr(),
  transport_days_proposed: DS.attr(),
  compensation_days_manual: DS.attr(),
  compensation_days_proposed: DS.attr(), 
  accommodation_cost: DS.attr(),
  accommodation_default_currency: DS.attr({'choices': CHOICES.CURRENCIES}),
  accommodation_payment_way: DS.attr({'choices': CHOICES.WAYS_OF_PAYMENT}),
  accommodation_payment_description: DS.attr(),
  transportation_default_currency: DS.attr({'choices': CHOICES.CURRENCIES}),
  transportation_payment_way: DS.attr({'choices': CHOICES.WAYS_OF_PAYMENT}),
  transportation_payment_description: DS.attr(),
  overnights_num_manual: DS.attr(),
  overnight_cost: DS.attr(),
  compensation_level: DS.attr(),
  same_day_return_task: DS.attr('boolean', {attrs: {disabled: true}}),
});
