import validate from 'ember-gen/validate';
import { field } from 'ember-gen';
import meta from 'travel/lib/meta';
import PROFILE from '../common/profile';
import SECRETARY from '../application/secretary';
import CONTROLLER from '../application/controller';
import { fileField } from '../../lib/common';

const FS_VALIDATORS = {
  project: [validate.presence(true)],
  reason: [validate.presence(true)],
  task_start_date: [validate.presence(true)],
  task_end_date: [validate.presence(true)],
  user_recommendation: [validate.length({ max: 255, allowBlank: true })],
  travel_files: [validate.presence(true)],
  transportation_type: [validate.presence(true)],
}

const FS_CREATE_1 = [
  {
    label: 'application.label',
    text: 'submit.action.explanatory.text',
    fields: [
      field('dse', { disabled: true }),
      'project',
      'reason',
      'task_start_date',
      'task_end_date',
      meta.forms.travel_info,
      'participation_local_cost',
      'participation_local_currency',
      'user_recommendation',
      'transportation_type',
    ],
    layout: {
      flex: [50, 50, 100, 50, 50, 100, 50, 50, 100, 100],
    },
  },
];

const FS_EDIT_1 = FS_CREATE_1;

const FS_EDIT_6 = [
  {
    label: 'application.label',
    text: 'submit.action.explanatory.text',
    fields: [
      field('dse', { disabled: true }),
      field('project', { disabled: true }),
      field('reason', { disabled: true }),
      'manager_movement_approval',
      'withdrawn',
      field('task_start_date', { disabled: true }),
      field('task_end_date', { disabled: true }),
      meta.forms.travel_info,
    ],
    layout: {
      flex: [50, 50, 100, 50, 50, 50, 50, 100],
    },
  },
  {
    label: 'compensation.label',
    fields: [
      fileField('travel_files', 'application-item', 'travel_files', {},
      {
	multiple: true
      }),
      'additional_expenses',
      'additional_expenses_local_currency',
      'additional_expenses_description',
    ],
    layout: {
      flex: [100, 50, 50, 100],
    },
  },
];

const FS_VIEW_1 = [
  PROFILE.FS_DETAILS,
  {
    label: 'application.label',
    fields: [
      'dse',
      'project.name',
      'reason',
      'task_start_date_time_format',
      'task_end_date_time_format',
      meta.forms.travel_info,
      'participation_local_cost',
      'participation_local_currency',
      'user_recommendation',
      'status_label',
      'transportation_type',
    ],
    layout: {
      flex: [50, 50, 100, 50, 50, 100, 50, 50, 100, 50, 50],
    },
  },
];

const FS_VIEW_4 = SECRETARY.FS_VIEW_3;

const FS_VIEW_6 = [
  {
    label: 'application.label',
    fields: [
      'dse',
      'project.name',
      'reason',
      'manager_movement_approval',
      'withdrawn',
      'task_start_date_time_format',
      'task_end_date_time_format',
      meta.forms.travel_info,
    ],
    layout: {
      flex: [50, 50, 100, 50, 50, 50, 50, 100],
    },
  },
  {
    label: 'compensation.label',
    fields: [
      fileField('travel_files', 'application-item', 'travel_files',
      {
        readonly: true
      },
      {
        preventDelete: true
      }),
      'additional_expenses',
      'additional_expenses_local_currency',
      'additional_expenses_description',
      'status_label',
    ],
    layout: {
      flex: [100, 50, 50, 100, 100],
    },
  },
];

const FS_VIEW_8 = CONTROLLER.FS_VIEW_8;

export { FS_CREATE_1, FS_EDIT_1, FS_EDIT_6, FS_VIEW_1, FS_VIEW_4, FS_VIEW_6, FS_VIEW_8, FS_VALIDATORS };
