import validate from 'ember-gen/validate';
import { field } from 'ember-gen';
import meta from 'travel/lib/meta';
import PROFILE from '../common/profile';
import { fileField } from '../../lib/common';

const FS_VALIDATORS = {
  project: [validate.presence(true)],
  reason: [validate.presence(true)],
  task_start_date: [validate.presence(true)],
  task_end_date: [validate.presence(true)],
  compensation_petition_date: [validate.presence(true)],
  compensation_petition_protocol: [validate.presence(true)],
  compensation_decision_date: [validate.presence(true)],
  compensation_decision_protocol: [validate.presence(true)],
};

const FS_EDIT_8 = [
  {
    label: 'travel_info.label',
    text: 'submit.action.explanatory.text',
    fields: [
      'dse',
      field('project', { disabled: true }),
      field('first_name', { disabled: true }),
      field('last_name', { disabled: true }),
      field('tax_reg_num', { disabled: true }),
      field('iban', { disabled: true }),
      field('reason', { disabled: true }),
      'manager_movement_approval',
      'withdrawn',
      'task_start_date',
      'task_end_date',
      meta.forms.travel_info,
      'participation_cost',
      'participation_local_cost',
      'participation_local_currency',
      'participation_payment_way',
      'non_grnet_quota',
    ],
    layout: {
      flex: [
        50, 50, 50, 50, 50, 50, 100, 50, 50,
        50, 50, 100, 50, 30, 20, 50, 50,
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
      'additional_expenses_grnet',
    ],
    layout: {
      flex: [100, 50, 50, 100, 100],
    },
  },
  {
    label: 'protocol.label',
    fields: [
      field('expenditure_date_protocol', { disabled: true }),
      field('expenditure_protocol', { disabled: true }),
      field('movement_date_protocol', { disabled: true }),
      field('movement_protocol', { disabled: true }),
      'compensation_petition_date',
      'compensation_petition_protocol',
      'compensation_decision_date',
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
      field('compensation_final', { disabled: true }),
      'total_cost_calculated',
    ],
    layout: {
      flex: [
        50, 50, 50, 50, 50, 100,
      ],
    },
  },
];

const FS_VIEW_8 = [
  PROFILE.FS_DETAILS,
  {
    label: 'travel_info.label',
    fields: [
      'dse',
      'project.name',
      'reason',
      'manager_movement_approval',
      'withdrawn',
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
        50, 50, 100, 50, 50, 50, 50, 100,
        50, 30, 20, 50, 50
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
      'additional_expenses_grnet',
    ],
    layout: {
      flex: [100, 50, 50, 100, 100],
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

export { FS_EDIT_8, FS_VIEW_8, FS_VALIDATORS };
