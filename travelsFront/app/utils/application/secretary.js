import Ember from 'ember';
import {field} from 'ember-gen';
import meta from 'travel/lib/meta';
import PROFILE from '../common/profile';


const FS_EDIT_3 = [
  {
    label: 'travel_info.label',
    fields: [
      field('first_name', { disabled: true }),
      field('last_name', { disabled: true }),
      'dse',
      'project',
      'reason',
      field('user_recommendation', {disabled: true}),
      'task_start_date',
      'task_end_date',
      meta.forms.travel_info,
      'additional_expenses_initial',
      'additional_expenses_initial_description',
      'participation_cost',
      'participation_local_cost',
      'participation_local_currency',
      'participation_payment_way',
      'non_grnet_quota',
    ],
    layout: {
      flex: [
        50, 50, 50, 50, 100, 100, 50, 50,
        100, 50, 50, 50, 30, 20, 50, 50, 15
      ]
    }
  },
  {
  label: 'protocol.label',
    fields: [
      'expenditure_date_protocol',
      'expenditure_protocol',
      'movement_date_protocol',
      'movement_protocol',
    ],
    layout: {
      flex: [
        50, 50, 50, 50
      ]
    }
  },
  {
    label: 'computed_data.label',
    fields: [
      'overnights_sum_cost',
      'trip_days_before',
      'compensation_cost',
      'trip_days_after',
      'total_cost_calculated'
    ],
    layout: {
      flex: [
        50, 50, 50, 50, 100
      ]
    }
  }
];

const FS_VIEW_3 = [
  PROFILE.FS_DETAILS,
  {
    label: 'travel_info.label',
    fields: [
      'dse',
      'project.name',
      'reason',
      field('user_recommendation', {disabled: true}),
      'task_start_date_time_format',
      'task_end_date_time_format',
      meta.forms.travel_info,
      'additional_expenses_initial',
      'additional_expenses_initial_description',
      'participation_cost',
      'participation_local_cost',
      'participation_local_currency',
      'participation_payment_way_label',
      'non_grnet_quota',
    ],
    layout: {
      flex: [
        50, 50, 100, 100, 50, 50,
        100, 50, 50, 50, 30, 20, 50, 50, 15
      ]
    }
  },
  {
  label: 'protocol.label',
    fields: [
      'expenditure_date_protocol',
      'expenditure_protocol',
      'movement_date_protocol',
      'movement_protocol',
    ],
    layout: {
      flex: [
        50, 50, 50, 50
      ]
    }
  },
  {
    label: 'computed_data.label',
    fields: [
      'overnights_sum_cost',
      'trip_days_before',
      'compensation_cost',
      'trip_days_after',
      'total_cost_calculated'
    ],
    layout: {
      flex: [
        50, 50, 50, 50, 100
      ]
    }
  }
];

export { FS_EDIT_3, FS_VIEW_3 };