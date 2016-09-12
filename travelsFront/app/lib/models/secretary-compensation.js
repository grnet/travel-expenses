import {Compensation} from 'travels-front/lib/models/compensation';
import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travels-front/config/environment'; 

const CHOICES = ENV.APP.resource_choices,
      CURRENCY = [[ENV.default_currency, ENV.default_currency]];

export var SecretaryCompensation = Compensation.extend({
     
  //secretary fields
  compensation_petition_date: DS.attr('date'),
  compensation_petition_protocol: DS.attr(),
  compensation_decision_date: DS.attr('date'),
  compensation_decision_protocol: DS.attr(),
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
  expenditure_date_protocol: DS.attr('date'),
  expenditure_protocol: DS.attr(),
  movement_date_protocol: DS.attr('date'),
  movement_protocol: DS.attr(),
  trip_days_before: DS.attr(),
  trip_days_after: DS.attr(),
  overnights_sum_cost: DS.attr(),
  overnights_proposed: DS.attr(),
  overnights_num: DS.attr(),
  compensation_final: DS.attr(),
  total_cost: DS.attr(),

  //Travel_info DATA
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
  same_day_return_task: DS.attr(),
  
  
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
