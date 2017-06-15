import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travels-front/config/environment';

const CHOICES = ENV.APP.resource_choices;
const CURRENCY = [[ENV.default_currency, ENV.default_currency]];

const UI_USER = {
  fieldsets: [
    {
      'label': 'travel_info.travel',
      'fields': ['departure_point', 'arrival_point', 'depart_date', 'return_date']
    },
    {
      'label': 'travel_info.extra',
      'fields': ['meals', 'means_of_transport']
    },
  ],
  layout: {
    flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
  }
};

const UI_MANAGER = {
  fields: ['departure_point']
}


export default DS.Model.extend({
  __api__: {
    ns: 'petition'
  },
  __ui__: {
    'user': UI_USER,
    'manager': UI_MANAGER
  },
  url: DS.attr(),
  departure_point: DS.belongsTo('city', {attrs: {required: true, autocomplete: true}}),
  arrival_point: DS.belongsTo('city', {attrs: {required: true, autocomplete: true}}),
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
  meals: DS.attr({'choices': CHOICES.MEALS, defaultValue: 'FULL'}),
  means_of_transport: DS.attr({'choices': CHOICES.TRANSPORTATION}),
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

  tabLabel: Ember.computed('id', function() {
    return "Destination: " + (this.get('id') || 'New');
  })
});
