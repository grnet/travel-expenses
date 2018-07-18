import Ember from 'ember';
import { field } from 'ember-gen';
import TRAVEL_INFO from '../utils/application/travel-info';

const {
  get,
  computed,
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
        departure_point: last.get('changeset.arrival_point') || undefined,
        accommodation_local_currency: 'EUR',
      });
    } else {
      let default_departure_point_id = 204; // TODO: make this dynamic using config/environment

      // cities may not be loaded yet, use findRecord to ensure resolved city record
      return store.findRecord('city', default_departure_point_id).then((city) => {
        return store.createRecord('travel-info', {
          departure_point: city,
          accommodation_local_currency: 'EUR',
        })
      });
    }
  },
  disabled: computed(function() {
    let role = this.get('user.user_group');
    let status = this.get('model.status');
    if (role === 'USER' || role === 'MANAGER') {
      if (status >= 5 && status <= 6) {
        return true;
      }
    }
  }),
  modelMeta: {
    fieldsets: computed(function() {
      let session = this.container.lookup('service:session');
      let role = session.get('session.authenticated.user_group');
      let res = [{}];
      if (role === 'USER' || role === 'MANAGER') {
        res = TRAVEL_INFO.FS_EDIT_1_USER;
      } else if (role === 'SECRETARY') {
        res = TRAVEL_INFO.FS_EDIT_3_SECRETARY;
      } else if (role === 'CONTROLLER') {
        res = TRAVEL_INFO.FS_EDIT_8_CONTROLLER;
      } else if (role === 'VIEWER') {
        res = TRAVEL_INFO.FS_VIEW_VIEWER;
      }

      return res;
    }),
    validators: computed(function() {
      let session = this.container.lookup('service:session');
      let role = session.get('session.authenticated.user_group');
      let val = {};

      if (role === 'USER') {
        val = TRAVEL_INFO.FS_USER_VALIDATORS;
      } else if (role === 'SECRETARY') {
        val = TRAVEL_INFO.FS_SECRETARY_VALIDATORS;
      } else if (role === 'CONTROLLER') {
        val = TRAVEL_INFO.FS_CONTROLLER_VALIDATORS;
      }

      return val;
    }),
  },
})

export let forms = { travel_info }
