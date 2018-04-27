import DS from 'ember-data';
import Ember from 'ember';
import ENV from 'travel/config/environment';
import { computeDateFormat } from '../lib/common';
import { computeDateTimeFormat } from '../lib/common';

const CHOICES = ENV.APP.resources;

export default DS.Model.extend({
  __api__: {
    path: 'applications',

    serialize(hash, snapshot, serializer) {
      if (hash['travel_files'] === '') {
        return hash;
      }
      delete hash['travel_files'];
      return hash;
    }
  },

  session: Ember.inject.service('session'),
  // profile fields
  first_name: DS.attr(),
  last_name: DS.attr(),
  specialty: DS.attr({ 'choices': CHOICES.SPECIALTY }),
  kind: DS.attr({ 'choices': CHOICES.KIND }),
  tax_reg_num: DS.attr(),
  tax_office: DS.belongsTo('tax-office', { formAttrs: { optionLabelAttr: 'full_label' } }),
  iban: DS.attr(),
  user_category: DS.attr({ 'choices': CHOICES.USER_CATEGORY, disabled: true }),
  // application - user fields
  user: DS.attr('string'),
  dse: DS.attr('string'),
  project: DS.belongsTo('project', { autocomplete: true, formAttrs: { optionLabelAttr: 'name' } }),
  reason: DS.attr({ type: 'text' }),
  participation_local_cost: DS.attr(),
  participation_local_currency: DS.attr({ 'choices': CHOICES.CURRENCIES, autocomplete: true }),
  task_start_date: DS.attr('date', {
    formAttrs: {
      time: true,
      format: 'dd mmmm yyyy',
    },
  }),
  task_end_date: DS.attr('date', {
    formAttrs: {
      time: true,
      format: 'dd mmmm yyyy',
    },
  }),
  task_start_date_format: computeDateFormat('task_start_date'),
  task_end_date_format: computeDateFormat('task_end_date'),
  task_start_date_time_format: computeDateTimeFormat('task_start_date'),
  task_end_date_time_format: computeDateTimeFormat('task_end_date'),
  user_recommendation: DS.attr({ type: 'text' }),
  status: DS.attr({ type: 'select', 'choices': CHOICES.STATUS }),
  travel_info: DS.hasMany('travel-info', { displayComponent: 'display-travel-info' }),
  // application - secretary fields
  additional_expenses_initial: DS.attr(),
  additional_expenses_initial_description: DS.attr(),
  expenditure_date_protocol: DS.attr('date'),
  expenditure_date_protocol_format: computeDateFormat('expenditure_date_protocol'),
  expenditure_protocol: DS.attr(),
  movement_date_protocol: DS.attr('date'),
  movement_date_protocol_format: computeDateFormat('movement_date_protocol'),
  movement_protocol: DS.attr(),
  non_grnet_quota: DS.attr(),
  manager_movement_approval: DS.attr('boolean'),
  participation_cost: DS.attr(),
  participation_payment_way: DS.attr({ 'choices': CHOICES.WAYS_OF_PAYMENT }),
  trip_days_before: DS.attr(),
  trip_days_after: DS.attr({ disabled: true }),
  overnights_sum_cost: DS.attr({ disabled: true }),
  compensation_cost: DS.attr({ disabled: true }),
  total_cost_calculated: DS.attr({ disabled: true }),
  withdrawn: DS.attr('boolean'),
  // compensation - user fields
  additional_expenses: DS.attr(),
  additional_expenses_local_currency: DS.attr({ 'choices': CHOICES.CURRENCIES, autocomplete: true }),
  additional_expenses_description: DS.attr({ type: 'text' }),
  travel_files: DS.attr(),
  // compensation - controller fields
  compensation_petition_date: DS.attr('date'),
  compensation_petition_date_format: computeDateFormat('compensation_petition_date'),
  compensation_petition_protocol: DS.attr(),
  compensation_decision_date: DS.attr('date'),
  compensation_decision_date_format: computeDateFormat('compensation_decision_date'),
  compensation_decision_protocol: DS.attr(),
  timesheeted: DS.attr('boolean'),

  // set status label value
  status_label: Ember.computed('status', function() {
    var status = this.get('status');
    var label = CHOICES.STATUS[status - 1];

    return label[1] || status;
  }),

  specialty_label: Ember.computed('specialty', function() {
    let specialty = this.get('specialty');

    for (let pair of CHOICES.SPECIALTY) {
      if (pair[0] === specialty) {
        return pair[1] || specialty;
      }
    }
  }),

  kind_label: Ember.computed('kind', function() {
    let kind = this.get('kind');

    for (let pair of CHOICES.KIND) {
      if (pair[0] === kind) {
        return pair[1] || kind;
      }
    }
  }),

  participation_payment_way_label: Ember.computed('participation_payment_way', function() {
    let participation_payment_way = this.get('participation_payment_way');

    for (let pair of CHOICES.WAYS_OF_PAYMENT) {
      if (pair[0] === participation_payment_way) {
        return pair[1] || participation_payment_way;
      }
    }
  }),
});
