import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travel/config/environment';
import {computeDateTimeFormat} from '../lib/common';

const {
  get, set
} = Ember;

const CHOICES = ENV.APP.resources;
const CURRENCY = ENV.APP.currency || ['EUR', 'Euro'];


export default DS.Model.extend({
  url: DS.attr(),
  departure_point: DS.belongsTo('city', {required: true, autocomplete: true, displayAttr: 'labelWithCountry'}),
  arrival_point: DS.belongsTo('city', {required: true, autocomplete: true, displayAttr: 'labelWithCountry'}),
  depart_date: DS.attr('date', {
    formAttrs: {
      time: true,
      format: "dd mmmm yyyy"
    }
  }),
  return_date: DS.attr('date', {
    formAttrs: {
      time: true,
      format: "dd mmmm yyyy"
    }
  }),
  depart_date_time_format: computeDateTimeFormat('depart_date'),
  return_date_time_format: computeDateTimeFormat('return_date'),
  meals: DS.attr({'choices': CHOICES.MEALS, defaultValue: 'NON'}),
  means_of_transport: DS.attr({'choices': CHOICES.TRANSPORTATION, defaultValue: 'AIR'}),
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
  index: DS.attr(),
  overnights_num_proposed: DS.attr(),

  tabDisplay: Ember.computed('arrival_point.name', 'departure_point.name', function() {
    let departure = get(this, 'departure_point.name') || '';
    let destination = get(this, 'arrival_point.name') || '';
    return `${departure} → ${destination}`;
  })
});
