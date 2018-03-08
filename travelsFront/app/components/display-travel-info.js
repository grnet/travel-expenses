import Ember from 'ember';
import {field} from 'ember-gen';
import TravelInfo from 'travel/models/travel-info';
import {resourceMetaFrom} from 'ember-gen/lib/meta';

export default Ember.Component.extend({
  modelMeta: Ember.computed(function() {
    let meta = {
    fieldsets: Ember.computed(function() {
      let session = this.container.lookup('service:session');
      let role = session.get('session.authenticated.user_group');
      let res = [];
      if (role === 'USER' || role === 'MANAGER') {
        res = [{
        fields: [
          field('departure_point', { required: true }),
          field('arrival_point', { required: true }),
          'depart_date_time_format',
          'return_date_time_format',
        ],
        layout: {
          flex: [
            50, 50, 50, 50
          ]
        }
      }]
      } else if (role === 'SECRETARY') {
      res = [
      {
        fields: [
          field('departure_point', { required: true }),
          field('arrival_point', { required: true }),
          'depart_date_time_format',
          'return_date_time_format',
          'transport_days_manual',
          'transport_days_proposed',
          'means_of_transport_label',
          'transportation_cost',
          'transportation_payment_way_label',
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
          'meals_label',
          'accommodation_payment_way_label',
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
      ];
    }
      return res;
    }),};
    let model = TravelInfo;
    return resourceMetaFrom(TravelInfo, meta, model, Ember.getOwner(this));
  }),

});
