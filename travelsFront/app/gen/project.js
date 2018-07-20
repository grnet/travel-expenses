import gen from 'ember-gen/lib/gen';
import { field } from 'ember-gen';

const {
  get,
  computed,
  computed: { reads },
} = Ember;

export default gen.CRUDGen.extend({
  modelName: 'project',
  auth: true,
  _metaMixin: {
    session: Ember.inject.service(),
    role: reads('session.session.authenticated.user_group'),
  },
  list: {
    layout: 'table',
    menu: {
      order: 400,
      display: computed('role', function() {
        let role = get(this, 'role');
        if (role === 'HELPDESK') {
          return true;
        } else {
          return false;
        }
      }),
      icon: 'work',
      label: 'projects.tab',
    },
    page: {
      title: 'projects.page.title',
    },
    filter: {
      active: true,
      meta: {
        fields: [
          field('project', { modelName:'project', type: 'model', displayAttr: 'name' }),
        ]
      },
      serverSide: true,
      search: true,
      searchFields: ['name'],
    },
    sort: {
      active: true,
      serverSide: true,
      fields: ['name'],
    },
    paginate: {
      limits: [ 10, 50],
      serverSide: true,
      active: true,
    },
    row: {
      fields: [
        'name',
        'accounting_code',
        'manager.full_name',
      ],
      actions: ['gen:details', 'gen:edit'],
    },
  },
  details: {
    fieldsets: [{
      label: 'project_data.label',
      fields: [
        field('name', { type: 'text' }),
        'accounting_code',
        'manager.full_name',
      ],
      layout: {
        flex: [100, 100, 100],
      },
    }]
  },
  create: {
    fieldsets: [{
      label: 'project_data.label',
      fields: [
        field('name', { type: 'text' }),
        'accounting_code',
        'manager',
      ],
      layout: {
        flex: [100, 100, 100],
      },
    }]
  },
  edit: {
    fieldsets: [{
      label: 'project_data.label',
      fields: [
        field('name', { type: 'text' }),
        'accounting_code',
        'manager',
      ],
      layout: {
        flex: [100, 100, 100],
      },
    }]
  },
});
