import Ember from 'ember';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';


const {
  get
} = Ember;


const travel_info = field('travel_info', {

  // travel-info entry label
  entryLabel: Ember.computed('changeset.departure_point.name', 'changeset.arrival_point.name', function() {
    let changeset = get(this, 'changeset');
    let departure = get(changeset, 'departure_point.name') || '';
    let arrival = get(changeset, 'arrival_point.name') || '';
    return `${departure} → ${arrival}`;
  }),

  // field label
  label: 'travel.info.label',
  createEntry: function(field, store) {
    // `this` is the component context
    let last = this.get('value.lastObject');
    if (last) {
      return store.createRecord('travel-info', { 
        departure_point: last.get('changeset.arrival_point') || undefined
      });
    } else {
      let default_departure_point_id = 15; //TODO: make this dynamic using config/environment
      // cities may not be loaded yet, use findRecord to ensure resolved city record
      return store.findRecord('city', default_departure_point_id).then((city) => {
        return store.createRecord('travel-info', {
          departure_point: city
        })
      });
    }
  },

  modelMeta: {
    fieldsets: [
      {
        fields: [
          field('departure_point', { required: true }),
          field('arrival_point', { required: true }),
          field('depart_date', {}),
          field('return_date', {}),
          'transport_days_manual',
          'transport_days_proposed',
          'means_of_transport',
          'transportation_cost',
          'transportation_payment_way',
        ],
        layout: {
          flex: [
            50, 50, 50, 50, 50, 50, 50, 50, 100
          ]
        }
      },
      {
        label: 'travel_info.accommodation.label',
        fields: [
          'overnights_num_manual',
          'overnights_num_proposed',
          'accommodation_cost',
          'accommodation_local_cost',
          'accommodation_local_currency',
          'meals',
          'accommodation_payment_way',
        ],
        layout: {
          flex: [
            50, 50, 50, 30, 20, 50, 50
          ]
        }
      },
      {
        label: 'travel_info.compensation.label',
        fields: [
          'compensation_days_manual',
          'compensation_days_proposed',
          'compensation_level',
        ],
        layout: {
          flex: [
            50, 50, 50
          ]
        }
      },
    ]
  }
})


export let forms = { travel_info }
