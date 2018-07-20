import gen from 'ember-gen/lib/gen';
import { field } from 'ember-gen';

const {
  get,
  computed,
  computed: { reads },
} = Ember;

export default gen.CRUDGen.extend({
  modelName: 'city',
  auth: true,
  _metaMixin: {
    session: Ember.inject.service(),
    role: reads('session.session.authenticated.user_group'),
  },
  list: {
    layout: 'table',
    menu: {
      display: computed('role', function() {
        let role = get(this, 'role');
        if (role === 'HELPDESK') {
          return true;
        } else {
          return false;
        }
      }),
      icon: 'place',
      label: 'cities.tab',
    },
    page: {
      title: 'cities.page.title',
    },
    filter: {
      active: true,
      meta: {
        fields: [
          field('city', { modelName:'city', type: 'model', displayAttr: 'name' }),
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
        field('name', { label: 'city_name.label' }),
        'country.name',
        'timezone',
      ],
      actions: ['gen:details'],
    },
  },
  details: {
    fieldsets: [{
      label: 'city_data.label',
      fields: [
        field('name', { label: 'city_name.label' }),
        'country.name',
        'timezone',
      ],
      layout: {
        flex: [100, 100, 100],
      },
    }]
  },
  create: {
    fieldsets: [{
      label: 'city_data.label',
      fields: [
        field('name', { label: 'city_name.label' }),
        'country',
        'timezone',
      ],
      layout: {
        flex: [100, 100, 100],
      },
    }]
  },
  edit: {
    fieldsets: [{
      label: 'city_data.label',
      fields: [
        field('name', { label: 'city_name.label' }),
        'country',
        'timezone',
      ],
      layout: {
        flex: [100, 100, 100],
      },
    }]
  },
});
