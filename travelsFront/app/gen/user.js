import gen from 'ember-gen/lib/gen';
import { field } from 'ember-gen';
import PROFILE from '../utils/common/profile';
import { applicationActions } from '../utils/common/actions';

const {
  get,
  computed,
  computed: { reads },
} = Ember;

export default gen.CRUDGen.extend({
  resourceName: 'users',
  modelName: 'user',
  auth: true,
  _metaMixin: {
    session: Ember.inject.service(),
    role: reads('session.session.authenticated.user_group'),
  },
  list: {
    layout: 'table',
    menu: {
      order: 300,
      display: true,
      icon: 'supervisor_account',
      label: 'users.tab',
    },
    page: {
      title: 'users.page.title',
    },
    filter: {
      active: true,
      meta: {
        fields: [
          field('email'),
        ]
      },
      serverSide: true,
      search: true,
      searchFields: ['email'],
    },
    sort: {
      active: true,
      serverSide: true,
      fields: ['email'],
    },
    paginate: {
      limits: [ 10, 50],
      serverSide: true,
      active: true,
    },
    row: {
      fields: [
        'username',
        'first_name',
        'last_name',
        'email',
      ],
      actions: ['gen:details', 'gen:edit', 'activate'],
      actionsMap: {
        activate: applicationActions.activate,
      },
    },
  },
  details: {
    fieldsets: [{
      label: 'user_data.label',
      fields: [
        field('first_name'),
        field('last_name'),
        field('username'),
        field('email'),
        field('specialty_label'),
        field('kind_label'),
        field('tax_reg_num'),
        field('tax_office.name'),
        field('iban'),
        field('user_category'),
        field('user_group'),
      ],
      layout: {
        flex: [50, 50, 50, 50, 50, 50, 50, 50, 100, 50, 50],
      },
    }]
  },
  edit: {
    fieldsets: [{
      label: 'user_data.label',
      fields: [
        field('first_name'),
        field('last_name'),
        field('username'),
        field('email'),
      ],
      layout: {
        flex: [50, 50, 50, 50],
      },
    }]
  },
});

