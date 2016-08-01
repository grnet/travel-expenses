import {Petition} from 'travels-front/lib/models/petition';

export var SecretaryPetition = Petition.extend({
    // profile fields
  first_name: DS.attr({attrs: {disabled: true, required: true}}),
  last_name: DS.attr({attrs: {disabled: true, required: true}}),
  specialty: DS.attr({'label': 'Specialty', 'choices': CHOICES.SPECIALTY, attrs: {disabled: true}}),
  kind: DS.attr({'choices': CHOICES.KIND, attrs: {disabled: true}}),
  tax_reg_num: DS.attr({attrs: {disabled: true}, label: 'VAT'}),
  tax_office: DS.belongsTo('tax-office', {attrs: {disabled: true}}),
  iban: DS.attr({attrs: {disabled: true}}),
  user_category: DS.attr({'label': 'User Category', 'choices': CHOICES.USER_CATEGORY, attrs: {disabled: true}}),
  //petition fields
  user: DS.belongsTo('profile'),
  dse: DS.attr('string', {attrs: {disabled: true, required: true}}),
  project: DS.belongsTo('project', {attrs: {labelKey: "full_label", required: true}}),
  reason: DS.attr({attrs: {required: true, textarea: true}}),
  movement_category: DS.attr({choices: CHOICES.MOVEMENT_CATEGORIES, attrs: {disabled: true}}),
  country_category: DS.attr('string', {attrs: {disabled: true}}),
 	created: DS.attr(),
 	updated: DS.attr(),
  task_start_date: DS.attr('date', {
    attrs: {
      time: true,
      required: true    
    },
    label: 'Task starts at'
  }),
  task_end_date: DS.attr('date', {
    attrs: {
      time: true,
      required: true 
    },
    label: 'Task ends at'
  }),  
  status: DS.attr(),
  petition_id: Ember.computed('id', function(){
    // return just the status id
    return _.last(this.get('id').replace(/\/$/, '').split('/'));
  }),
  participation_local_cost: DS.attr({attrs: {required: true}}), 
  additional_expenses_initial: DS.attr({attrs: {required: true}}),
  non_grnet_quota: DS.attr({attrs: {required: true}}),
  user_recommendation: DS.attr({attrs:{textarea: true}}),
  
  //secretary fields
  participation_cost: DS.attr(),
  participation_local_currency: DS.attr(), 
  participation_default_currency: DS.attr(),
  participation_payment_way: DS.attr(),
  participation_payment_description: DS.attr(),
  additional_expenses_default_currency: DS.attr(),
  additional_expenses_initial_description: DS.attr(),
  travel_data: DS.attr({attrs:{textarea: true}}),
  movement_id: DS.attr(),
  expenditure_date_protocol: DS.attr(),
  expenditure_protocol: DS.attr(),
  movement_date_protocol: DS.attr(),
  movement_protocol: DS.attr(),
  trip_days_before: DS.attr(),
  trip_days_after: DS.attr(),
  overnights_sum_cost: DS.attr(),
  overnights_proposed: DS.attr(),
  overnights_num: DS.attr(),
  compensation_final: DS.attr(),
  total_cost: DS.attr(),

  //Travel_info DATA
  travel_info: DS.attr(),
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
  meals: DS.attr({'label': 'Meals', 'choices': CHOICES.MEALS}),
  means_of_transport: DS.attr({'label': 'Means of Transport', 'choices': CHOICES.TRANSPORTATION}),
  transportation_cost: DS.attr(),
  accommodation_local_cost: DS.attr(),
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
