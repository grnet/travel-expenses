import DS from 'ember-data';
import ENV from 'travel/config/environment';
import gen from 'ember-gen/lib/attrs';
import {computeDateFormat} from '../lib/common';
import {computeDateTimeFormat} from '../lib/common';


const CHOICES = ENV.APP.resources;
const CURRENCY = ENV.APP.currency || ['EUR', 'Euro'];


export default DS.Model.extend({
  __api__: {
    path: 'applications'
  },

  session: Ember.inject.service('session'),
  first_name: DS.attr(),
  last_name: DS.attr(),
  specialty: DS.attr({'choices': CHOICES.SPECIALTY}),
  kind: DS.attr({'choices': CHOICES.KIND}),
  tax_reg_num: DS.attr(),
  tax_office: DS.belongsTo('tax-office', {formAttrs: {optionLabelAttr: 'full_label'}}),
  iban: DS.attr(),
  user_category: DS.attr({'choices': CHOICES.USER_CATEGORY, attrs: {disabled: true}}),
  //application fields
  user: DS.attr('string'),
  dse: DS.attr('string', {required: true}),
  project: DS.belongsTo('project', {required: true, autocomplete: true, formAttrs: {optionLabelAttr: 'name'}}),
  reason: DS.attr({attrs: {required: true, textarea: true}}),
  created: DS.attr('date', {time: true, required: true}),
  updated: DS.attr('date', {time: true, required: true}),
  participation_local_cost: DS.attr(),
  participation_local_currency: DS.attr({'choices': CHOICES.CURRENCIES, autocomplete: true}),
  task_start_date: DS.attr('date', {
    formAttrs: {
      time: true,
      format: "dd mmmm yyyy"
    },
    required: true
  }),
  task_end_date: DS.attr('date', {
    formAttrs: {
      time: true,
      format: "dd mmmm yyyy"
    },
    required: true
  }),
  task_start_date_format: computeDateFormat('task_start_date'),
  task_end_date_format: computeDateFormat('task_end_date'),
  task_start_date_time_format: computeDateTimeFormat('task_start_date'),
  task_end_date_time_format: computeDateTimeFormat('task_end_date'),
  user_recommendation: DS.attr({attrs:{textarea: true}}),
  status: DS.attr({'choices': CHOICES.STATUS, attrs: {disabled: true}}),
  petition_id: Ember.computed('id', function(){
  // return just the status id
    return _.last(this.get('id').replace(/\/$/, '').split('/'));
  }),
  travel_info: DS.hasMany('travel-info', {displayComponent: 'display-travel-info'}),
  // set status label value
  status_label: Ember.computed('status', function() {
    var status =this.get('status');
    var label=CHOICES.STATUS[status-1];
    return label[1] || status;
  }),

  specialty_label: Ember.computed('specialty', function() {
    let specialty =this.get('specialty');
    for (let pair of CHOICES.SPECIALTY) {
      if (pair[0] === specialty) {
        return pair[1] || specialty;
      }
    }
  }),

  kind_label: Ember.computed('kind', function() {
    let kind =this.get('kind');
    for (let pair of CHOICES.KIND) {
      if (pair[0] === kind) {
        return pair[1] || kind;
      }
    }
  }),
});
