import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travel/config/environment';
import { computeDateTimeFormat } from '../lib/common';

const {
  get, set,
} = Ember;

const CHOICES = ENV.APP.resources;
const CURRENCY = ENV.APP.currency || ['EUR', 'Euro'];

export default DS.Model.extend({
  session: Ember.inject.service('session'),

  url: DS.attr(),
  departure_point: DS.belongsTo('city', { autocomplete: true, displayAttr: 'labelWithCountry' }),
  arrival_point: DS.belongsTo('city', { autocomplete: true, displayAttr: 'labelWithCountry' }),
  depart_date: DS.attr('date', {
    formAttrs: {
      time: true,
      format: 'dd mmmm yyyy',
    },
  }),
  return_date: DS.attr('date', {
    formAttrs: {
      time: true,
      format: 'dd mmmm yyyy',
    },
  }),
  depart_date_time_format: computeDateTimeFormat('depart_date'),
  return_date_time_format: computeDateTimeFormat('return_date'),
  meals: DS.attr({ 'choices': CHOICES.MEALS, defaultValue: 'NON' }),
  overnights_num_proposed: DS.attr({ disabled: true }),
  accommodation_total_cost: DS.attr(),
  accommodation_total_local_cost: DS.attr(),
  accommodation_local_currency: DS.attr({ 'choices': CHOICES.CURRENCIES, autocomplete: true }),
  accommodation_payment_way: DS.attr({ 'choices': CHOICES.WAYS_OF_PAYMENT }),
  means_of_transport: DS.attr({ 'choices': CHOICES.TRANSPORTATION, defaultValue: 'AIR' }),
  transport_days_proposed: DS.attr({ disabled: true }),
  transportation_cost: DS.attr(),
  transportation_payment_way: DS.attr({ 'choices': CHOICES.WAYS_OF_PAYMENT }),
  compensation_days_proposed: DS.attr({ disabled: true }),
  compensation_level: DS.attr({ disabled: true }),
  same_day_return_task: DS.attr('boolean', { attrs: { disabled: true } }),
  index: DS.attr(),

  tabDisplay: Ember.computed('arrival_point.name', 'departure_point.name', function() {
    let departure = get(this, 'departure_point.name') || '';
    let destination = get(this, 'arrival_point.name') || '';

    return `${departure} → ${destination}`;
  }),

  transportation_payment_way_label: Ember.computed('transportation_payment_way', function() {
    let transportation_payment_way = this.get('transportation_payment_way');

    for (let pair of CHOICES.WAYS_OF_PAYMENT) {
      if (pair[0] === transportation_payment_way) {
        return pair[1] || transportation_payment_way;
      }
    }
  }),

  accommodation_payment_way_label: Ember.computed('accommodation_payment_way', function() {
    let accommodation_payment_way = this.get('accommodation_payment_way');

    for (let pair of CHOICES.WAYS_OF_PAYMENT) {
      if (pair[0] === accommodation_payment_way) {
        return pair[1] || accommodation_payment_way;
      }
    }
  }),

  meals_label: Ember.computed('meals', function() {
    let meals = this.get('meals');

    for (let pair of CHOICES.MEALS) {
      if (pair[0] === meals) {
        return pair[1] || meals;
      }
    }
  }),

  means_of_transport_label: Ember.computed('means_of_transport', function() {
    let means_of_transport = this.get('means_of_transport');

    for (let pair of CHOICES.TRANSPORTATION) {
      if (pair[0] === means_of_transport) {
        return pair[1] || means_of_transport;
      }
    }
  }),
});
