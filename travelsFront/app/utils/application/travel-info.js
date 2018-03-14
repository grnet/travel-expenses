import Ember from 'ember';
import {field} from 'ember-gen';

const FS_EDIT_1_USER = [
  {
    fields: [
      field('departure_point', { required: true }),
      field('arrival_point', { required: true }),
      field('depart_date', {}),
      field('return_date', {}),
    ],
    layout: {
      flex: [
        50, 50, 50, 50
      ]
    }
  }
];

const FS_VIEW_1_USER = [
  {
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
  }
];

const FS_EDIT_3_SECRETARY = [
  {
    fields: [
      field('departure_point', { required: true }),
      field('arrival_point', { required: true }),
      field('depart_date', {}),
      field('return_date', {}),
      'transport_days_proposed',
      'means_of_transport',
      'transportation_cost',
      'transportation_payment_way',
    ],
    layout: {
      flex: [
        50, 50, 50, 50, 50, 50, 50, 50
      ]
    }
  },
  {
    label: 'travel_info.accommodation.label',
    fields: [
      'overnights_num_proposed',
      'meals',
      'accommodation_cost',
      'accommodation_local_cost',
      'accommodation_local_currency',
      'accommodation_payment_way',
    ],
    layout: {
      flex: [
        50, 50, 50, 30, 20, 50
      ]
    }
  },
  {
    label: 'travel_info.compensation.label',
    fields: [
      'compensation_days_proposed',
      'compensation_level',
    ],
    layout: {
      flex: [
        50, 50
      ]
    }
  }
];

const FS_VIEW_3_SECRETARY = [
  {
    fields: [
      field('departure_point', { required: true }),
      field('arrival_point', { required: true }),
      'depart_date_time_format',
      'return_date_time_format',
      'transport_days_proposed',
      'means_of_transport_label',
      'transportation_cost',
      'transportation_payment_way_label',
    ],
    layout: {
      flex: [
        50, 50, 50, 50, 50, 50, 50, 50
      ]
    }
  },
  {
    label: 'travel_info.accommodation.label',
    fields: [
      'overnights_num_proposed',
      'meals_label',
      'accommodation_cost',
      'accommodation_local_cost',
      'accommodation_local_currency',
      'accommodation_payment_way_label',
    ],
    layout: {
      flex: [
        50, 50, 50, 30, 20, 50
      ]
    }
  },
  {
    label: 'travel_info.compensation.label',
    fields: [
      'compensation_days_proposed',
      'compensation_level',
    ],
    layout: {
      flex: [
        50, 50
      ]
    }
  },
];

export { FS_EDIT_1_USER, FS_VIEW_1_USER, FS_EDIT_3_SECRETARY, FS_VIEW_3_SECRETARY };
