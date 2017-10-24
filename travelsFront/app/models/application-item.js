import DS from 'ember-data';
import ENV from 'travel/config/environment';


const CHOICES = ENV.APP.resources,
      CURRENCY = [[ENV.default_currency, ENV.default_currency]];


export default DS.Model.extend({
  __api__: {
    path: 'applications'
  },

  session: Ember.inject.service('session'),
  first_name: DS.attr(),
  last_name: DS.attr(),
  specialty: DS.attr({'choices': CHOICES.SPECIALTY, attrs: {disabled: true}}),
  kind: DS.attr({'choices': CHOICES.KIND, attrs: {disabled: true}}),
  tax_reg_num: DS.attr({attrs: {disabled: true}}),
  tax_office: DS.belongsTo('tax-office', {formAttrs: {optionLabelAttr: 'full_label'}}),
  iban: DS.attr({attrs: {disabled: true, required: true}}),
  user_category: DS.attr({'choices': CHOICES.USER_CATEGORY, attrs: {disabled: true}}),
  //petition fields
  user: DS.attr('string'),
  dse: DS.attr('string', {attrs: {required: true}}),
  project: DS.belongsTo('project', {formAttrs: {optionLabelAttr: 'name'}}),
  reason: DS.attr({attrs: {required: true, textarea: true}}),
  created: DS.attr('date', {time: true, required: true}),
  updated: DS.attr('date', {time: true, required: true}),
  task_start_date: DS.attr('date', {time: true}),
  task_end_date: DS.attr('date', {time: true}),
  participation_local_cost: DS.attr({attrs: {required: true}}),
  participation_local_currency: DS.attr({'choices': CURRENCY, 'component': 'petition-currency'}),
  additional_expenses_initial: DS.attr({attrs: {required: true}}),
  additional_expenses_initial_description: DS.attr({attrs:{textarea: true}}),
  user_recommendation: DS.attr({attrs:{textarea: true}}),
  status: DS.attr({'choices': CHOICES.STATUS, attrs: {disabled: true}}),
  petition_id: Ember.computed('id', function(){
    // return just the status id
    return _.last(this.get('id').replace(/\/$/, '').split('/'));
  }),

  arrival_point: DS.belongsTo('city', {autocomplete: true}),
  departure_point: DS.belongsTo('city', {autocomplete: true}),

  // set status label value
  status_label: Ember.computed('status', function() {
    var status =this.get('status');
    var label=CHOICES.STATUS[status-1];
    return label[1] || status;
  }),
});
