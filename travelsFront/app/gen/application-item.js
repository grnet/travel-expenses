import Ember from 'ember';
import gen from 'ember-gen/lib/gen';

const {
  get
} = Ember;


export default gen.CRUDGen.extend({
  order: 200,
  modelName: 'application_item',
  auth: true,
  path: 'applications',
  resourceName: 'applications',
  session: Ember.inject.service(),

  common: {
    preloadModels: [ 'city' ]
  },

  list: {
    preloadModels: ['project'],
    layout: 'table',
    menu: {
      display: true,
      icon: 'description',
      label: 'Αιτήσεις',
    },
    row: {
      fields: [
        'dse',
        'first_name',
        'last_name',
        'project.name',
        'task_start_date',
        'task_end_date',
        'arrival_point.name',
        'status_label',
      ],
      actions: ['gen:details', 'gen:edit'],
    }
  },


  details: {
    preloadModels: ['project'],
    page: {
      title: "Petition details",
    },
    fieldsets: [{
      fields: [
        'dse',
        'project.name',
        'first_name',
        'last_name',
        'task_start_date',
        'task_end_date',
        'arrival_point',
        'status_label',
      ],
      layout: {
        flex: [50, 50, 50, 50, 50, 50, 50, 50]
      }
    }],
  },

  create: {
    fieldsets: [{
      label: 'petition_create.title',
      fields: [
        'project',
        'reason',
        'task_start_date',
        'task_end_date',
        'arrival_point',
        'departure_point',
        'depart_date',
        'return_date',
        'participation_local_cost',
        'participation_local_currency',
        'user_recommendation',
      ],
      layout: {
        flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
      }
    }],
  },

  edit: {
    fieldsets: [{
      label: 'petition_create.title',
      fields: [
        'project',
        'reason',
        'task_start_date',
        'task_end_date',
        'arrival_point',
        'departure_point',
        'depart_date',
        'return_date',
        'participation_local_cost',
        'participation_local_currency',
        'user_recommendation',
      ],
      layout: {
        flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
      }
    }],
  },
});
