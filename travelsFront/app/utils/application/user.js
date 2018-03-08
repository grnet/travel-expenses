import Ember from 'ember';
import {field} from 'ember-gen';
import meta from 'travel/lib/meta';


const FS_CREATE_1 = {
  label: 'application_create.title',
  fields: [
    field('dse', {disabled: true}),
    'project',
    'reason',
    'task_start_date',
    'task_end_date',
    meta.forms.travel_info,
    'participation_local_cost',
    'participation_local_currency',
    'user_recommendation',
  ],
  layout: {
    flex: [50, 50, 100, 50, 50, 100, 50, 50, 100]
  }
}

const FS_EDIT_1 = FS_CREATE_1;

const FS_VIEW_1 = {
  label: 'application_create.title',
  fields: [
    field('dse', {disabled: true}),
    'project.name',
    'reason',
    'task_start_date_time_format',
    'task_end_date_time_format',
    meta.forms.travel_info,
    'participation_local_cost',
    'participation_local_currency',
    'user_recommendation',
    'status_label'
  ],
  layout: {
    flex: [50, 50, 100, 50, 50, 100, 50, 50, 100, 100]
  }
};

export {
  FS_CREATE_1,
  FS_EDIT_1,
  FS_VIEW_1
};
