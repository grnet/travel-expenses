import {SecretaryPetition} from 'travels-front/lib/models/secretary-petition';
import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travels-front/config/environment'; 

const CHOICES = ENV.APP.resource_choices,
      CURRENCY = [[ENV.default_currency, ENV.default_currency]];

export var Compensation = SecretaryPetition.extend({

  //compensation - user fields
  additional_expenses: DS.attr({attrs: {required: true}}),
  additional_expenses_local_currency: DS.attr({'choices': CURRENCY, 'component': 'petition-currency'}),
  additional_expenses_description: DS.attr({attrs:{textarea: true}}),
  travel_files: DS.attr('file', {attrs: {required: true}}),
  travel_report: DS.attr({attrs:{required: true, textarea: true}}),
});
