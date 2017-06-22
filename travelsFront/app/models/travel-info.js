import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travels-front/config/environment';

const {
  get, set
} = Ember;

const CHOICES = ENV.APP.resource_choices;
const CURRENCY = [[ENV.default_currency, ENV.default_currency]];

const UI_USER = {
  fields: [
    'departure_point', 'depart_date',
    'arrival_point', 'return_date'
  ],
  layout: {
    flex: [
      60, 40,
      60, 40
    ]
  }
};

const UI_SECRETARY = {
  fieldsets: [
    {
      'label': 'travel_info.transportation',
      'fields': ['departure_point', 'arrival_point', 'depart_date', 'return_date', 'means_of_transport', 'transportation_cost',
                'transportation_payment_way', 'transportation_payment_description']
    },
    {
      'label': 'travel_info.accommodation',
      'fields': ['compensation_level', 'meals', 'accommodation_cost', 'accommodation_local_cost', 'accommodation_local_currency',
                 'accommodation_payment_way', 'accommodation_payment_description']
    },
    {
      'label': 'computed_days.label',
      'fields': ['transport_days_manual', ['transport_days_proposed', {attrs:{disabled: true}}], 'overnights_num_manual', ['overnights_num_proposed', {attrs:{disabled: true}}],
      'compensation_days_manual', ['compensation_days_proposed', {attrs:{disabled: true}}]]
    },
  ],
  layout: {
    flex: [50, 50, 50, 50, 50, 50, 50, 50, 40, 10,
           50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
           50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
           50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
           50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
          ]
  }
};

const UI_CONTROLLER = {
  fieldsets: [
    {
      'label': 'travel_info.transportation',
      'fields': [['departure_point', {attrs:{disabled: true}}], ['arrival_point', {attrs:{disabled: true}}], ['depart_date', {attrs:{disabled: true}}],
       ['return_date', {attrs:{disabled: true}}], ['means_of_transport', {attrs:{disabled: true}}], 'transportation_cost', 
       'transportation_payment_way', 'transportation_payment_description',]
    },
    {
      'label': 'travel_info.accommodation',
      'fields': [['compensation_level', {attrs:{disabled: true}}], 'meals', 'accommodation_cost', 'accommodation_local_cost', 'accommodation_local_currency',
                 'accommodation_payment_way', 'accommodation_payment_description']
    },
    {
      'label': 'computed_days.label',
      'fields': ['transport_days_manual', ['transport_days_proposed', {attrs:{disabled: true}}], 'overnights_num_manual',
      ['overnights_num_proposed', {attrs:{disabled: true}}], 'compensation_days_manual', ['compensation_days_proposed', {attrs:{disabled: true}}]]
    },
  ],
  layout: {
    flex: [50, 50, 50, 50, 50, 50, 50, 50, 40, 10,
           50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
           50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
           50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
           50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
          ]
  }
}

const UI_MANAGER = {
  fieldsets: [
    {
      'label': 'travel_info.travel',
      'fields': ['departure_point', 'arrival_point', 'depart_date', 'return_date']
    },
  ],
  layout: {
    flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
  }
}


const normalizeTravelInfo = function(hash, serializer) {
  return hash;
}

let READONLY_FIELDS = [
  'url',
  'index',
  'same_day_return_task',
  'compensation_level',
  'overnight_cost',
  'compensation_days_manual',
  'compensation_days_proposed',
  'transport_days_manual',
  'transport_days_proposed'
];

const serializeTravelInfo = function(json, snapshot, serializer) {
  for (let field of READONLY_FIELDS) {
    delete json[field];
  }
  return json;
}

export default DS.Model.extend({
  __api__: {
    ns: 'petition',
    normalize: normalizeTravelInfo,
    serialize: serializeTravelInfo
  },
  __ui__: {
    'user': UI_USER,
    'secretary': UI_SECRETARY,
    'controller': UI_CONTROLLER,
    'manager': UI_MANAGER
  },
  url: DS.attr(),
  departure_point: DS.belongsTo('city', {attrs: {required: true, autocomplete: true}}),
  arrival_point: DS.belongsTo('city', {attrs: {required: true, autocomplete: true}}),
  depart_date: DS.attr('date', {
    attrs: {
      time: true
    }
  }),
  return_date: DS.attr('date', {
    attrs: {
      time: true
    }
  }),
  meals: DS.attr({'choices': CHOICES.MEALS, defaultValue: 'NON'}),
  means_of_transport: DS.attr({'choices': CHOICES.TRANSPORTATION, defaultValue: 'AIR'}),
  transportation_cost: DS.attr(),
  accommodation_local_cost: DS.attr(),
  accommodation_local_currency: DS.attr({'choices': CHOICES.CURRENCIES}),
  participation_local_currency: DS.attr({'choices': CHOICES.CURRENCIES}),
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
  index: DS.attr(),
  overnights_num_proposed: DS.attr(),

  tabDisplay: Ember.computed('arrival_point.name', 'departure_point.name', function() {
    let departure = get(this, 'departure_point.name') || '';
    let destination = get(this, 'arrival_point.name') || '';
    return `${departure} → ${destination}`;
  })
});
