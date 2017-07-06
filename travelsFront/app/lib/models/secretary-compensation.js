import {Compensation} from 'travels-front/lib/models/compensation';
import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travels-front/config/environment'; 

const CHOICES = ENV.APP.resource_choices,
      CURRENCY = [[ENV.default_currency, ENV.default_currency]];

export var SecretaryCompensation = Compensation.extend({
     
  //compensation - secretary fields  
  compensation_petition_date: DS.attr('date-simple'),
  compensation_petition_protocol: DS.attr(),
  compensation_decision_date: DS.attr('date-simple'),
  compensation_decision_protocol: DS.attr(),
  timesheeted: DS.attr('boolean'),
});
