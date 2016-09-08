import {Petition} from 'travels-front/lib/models/petition';
import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travels-front/config/environment'; 

const CHOICES = ENV.APP.resource_choices,
      CURRENCY = [[ENV.default_currency, ENV.default_currency]];

export var SecretaryPetition = Petition.extend({
     
  //secretary fields
  non_grnet_quota: DS.attr(),
  manager_travel_approval: DS.attr({attrs:{textarea: true}}),
  manager_final_approval: DS.attr({attrs:{textarea: true}}),
  participation_cost: DS.attr(),
  participation_default_currency: DS.attr({'choices': CHOICES.CURRENCIES}),
  participation_payment_way: DS.attr({'choices': CHOICES.WAYS_OF_PAYMENT}),
  participation_payment_description: DS.attr(),
  additional_expenses_default_currency: DS.attr({'choices': CHOICES.CURRENCIES}),
  secretary_recommendation: DS.attr({attrs:{textarea: true}}),
  movement_id: DS.attr(),
  expenditure_date_protocol: DS.attr('date-simple'),
  expenditure_protocol: DS.attr(),
  movement_date_protocol: DS.attr('date-simple'),
  movement_protocol: DS.attr(),
  trip_days_before: DS.attr(),
  trip_days_after: DS.attr({attrs: {disabled: true}}),
  overnights_sum_cost: DS.attr({attrs: {disabled: true}}),
  overnights_proposed: DS.attr({attrs: {disabled: true}}),
  overnights_num: DS.attr(),
  compensation_final: DS.attr({attrs: {disabled: true}}),
  total_cost: DS.attr({attrs: {disabled: true}}),

  //Travel_info DATA
  transport_days_manual: DS.attr(),
  transport_days_proposed: DS.attr({attrs: {disabled: true}}),
  compensation_days_manual: DS.attr(),
  compensation_days_proposed: DS.attr({attrs: {disabled: true}}), 
  accommodation_cost: DS.attr(),
  accommodation_default_currency: DS.attr({'choices': CHOICES.CURRENCIES}),
  accommodation_payment_way: DS.attr({'choices': CHOICES.WAYS_OF_PAYMENT}),
  accommodation_payment_description: DS.attr(),
  transportation_default_currency: DS.attr({'choices': CHOICES.CURRENCIES}),
  transportation_payment_way: DS.attr({'choices': CHOICES.WAYS_OF_PAYMENT}),
  transportation_payment_description: DS.attr(),
  overnights_num_manual: DS.attr(),
  overnight_cost: DS.attr(),
  compensation_level: DS.attr({attrs: {disabled: true}}),
  same_day_return_task: DS.attr('boolean', {attrs: {disabled: true}}),
});
