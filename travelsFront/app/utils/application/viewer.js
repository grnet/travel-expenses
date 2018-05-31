import { field } from 'ember-gen';
import meta from 'travel/lib/meta';
import { fileField } from '../../lib/common';

const FS_VIEW = [
  {
    label: 'application.label',
    fields: [
      'first_name',
      'last_name',
      'dse',
      'project.name',
      'reason',
      'task_start_date_time_format',
      'task_end_date_time_format',
      meta.forms.travel_info,
      'status_label',
    ],
    layout: {
      flex: [50, 50, 50, 50, 100, 50, 50, 100, 100],
    },
  },
];

export { FS_VIEW };
