import validate from 'ember-gen/validate';
import { field } from 'ember-gen';
import meta from 'travel/lib/meta';
import PROFILE from '../common/profile';
import USER from '../application/user';
import { fileField } from '../../lib/common';


const FS_VIEW = [
  PROFILE.FS_DETAILS,
  {
    label: 'travel_info.label',
    fields: [
      'dse',
      'project.name',
      'reason',
      'task_start_date_time_format',
      'task_end_date_time_format',
      meta.forms.travel_info,
      'participation_cost',
      'participation_local_cost',
      'participation_local_currency',
      'participation_payment_way_label',
      'non_grnet_quota',
    ],
    layout: {
      flex: [
        50, 50, 100, 50, 50,
        100, 50, 30, 20, 50, 50, 15,
      ],
    },
  },
  {
    label: 'compensation.label',
    fields: [
      fileField('travel_files', 'application-item', 'travel_files', {},
      {
        preventDelete: true
      }),
      'additional_expenses',
      'additional_expenses_local_currency',
      'additional_expenses_description',
    ],
    layout: {
      flex: [100, 50, 50, 100],
    },
  },
  {
    label: 'protocol.label',
    fields: [
      'expenditure_date_protocol_format',
      'expenditure_protocol',
      'movement_date_protocol_format',
      'movement_protocol',
      'compensation_petition_date_format',
      'compensation_petition_protocol',
      'compensation_decision_date_format',
      'compensation_decision_protocol',
    ],
    layout: {
      flex: [
        50, 50, 50, 50, 50, 50, 50, 50,
      ],
    },
  },
  {
    label: 'computed_data.label',
    fields: [
      'overnights_sum_cost',
      'trip_days_before',
      'compensation_cost',
      'trip_days_after',
      'compensation_final',
      'total_cost_calculated',
      'status_label',
    ],
    layout: {
      flex: [
        50, 50, 50, 50, 50, 100, 100,
      ],
    },
  },
];

const FS_CREATE_1 = USER.FS_CREATE_1;

const FS_EDIT_1 = USER.FS_EDIT_1;

const FS_EDIT_6 = USER.FS_EDIT_6;
 
export { FS_VIEW, FS_CREATE_1, FS_EDIT_1, FS_EDIT_6 };
