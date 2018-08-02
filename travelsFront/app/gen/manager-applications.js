import Ember from 'ember';
import gen from 'ember-gen/lib/gen';
import { field } from 'ember-gen';
import ENV from 'travel/config/environment';
import { applicationActions } from '../utils/common/actions';
import USER from '../utils/application/user';
import {abilityStates} from 'travel/lib/application/abilityStates';
import moment from 'moment';

const {
  get,
  computed,
  computed: { reads },
} = Ember;

const CHOICES = ENV.APP.resources;


export default gen.CRUDGen.extend({
  order: 200,
  modelName: 'application_item',
  auth: true,
  path: 'manager-applications',
  name: 'manager-applications',
  resourceName: 'applications',
  _metaMixin: {
    session: Ember.inject.service(),
    role: reads('session.session.authenticated.user_group'),
  },

  abilityStates: abilityStates,

  common: {
    preloadModels: ['city'],
    validators: computed('role', function() {
      let role = get(this, 'role');
      let val = {};

      if (role === 'MANAGER') {
        val = USER.FS_VALIDATORS;
      }

      return val;
    }),
  },

  list: {
    actions: ['gen:create'],
    actionsMap: {
      exportStats: applicationActions.exportStats,
    },
    preloadModels: ['project'],
    layout: 'table',
    menu: {
      display: true,
      icon: 'assignment_ind',
      label: 'my.appications.tab',
    },
    getModelQueryParams(qs) {
      if (qs && (qs.depart_date__gte || qs.depart_date__lte)) {
        qs.depart_date__gte = moment(qs.depart_date__gte).format("YYYY-MM-DD");
        qs.depart_date__lte = moment(qs.depart_date__lte).format("YYYY-MM-DD");
      }
      return qs
    },
    getModel(params, model) {
      let id = get(this, 'session.session.authenticated.id');
      return get(this, 'store').query('application-item', {user: id});
    },
    filter: {
      active: true,
      meta: {
        fields: computed(function() {
          let session = this.container.lookup('service:session');
          let role = session.get('session.authenticated.user_group');
          let res = [];

          if (role === 'MANAGER') {
            res = [
              field('project', { modelName:'project', type: 'model', displayAttr: 'name' }),
              field('status', { type:'select', choices: CHOICES.STATUS }),
            ]
          }
          return res;
        }),
      },
      serverSide: true,
      search: true,
      searchFields: ['dse', 'last_name'],
    },
    sort: {
      active: true,
      serverSide: true,
      fields: ['dse'],
    },
    paginate: {
      limits: [ 10, 50],
      serverSide: true,
      active: true,
    },
    row: {
      fields: [
        'dse',
        'first_name',
        'last_name',
        'project.name',
        'travel_info.lastObject.arrival_point.name',
        'task_start_date_format',
        'task_end_date_format',
        'status_label',
      ],
      actions: ['gen:details', 'gen:edit', 'markAsDeleted', 'submit', 'undo', 'pdf', 'approve', 'addToTimesheets', 'withdraw', 'managerApproval', 'reset'],
      actionsMap: {
        submit: applicationActions.submit,
        undo: applicationActions.undo,
        pdf: applicationActions.pdf,
        approve: applicationActions.approve,
        addToTimesheets: applicationActions.addToTimesheets,
        withdraw: applicationActions.withdraw,
        managerApproval: applicationActions.managerApproval,
        reset: applicationActions.reset,
        markAsDeleted: applicationActions.markAsDeleted,
      },
    },
  },

  details: {
    fieldsets: computed('role', function() {
      let role = get(this, 'role');
      let status = this.get('model.status');
      let res = [{}];

      if (role === 'MANAGER') {
        if (status >= 1 && status <= 3) {
          res = USER.FS_VIEW_1;
        } else if (status >= 4 && status <= 5) {
          res = USER.FS_VIEW_4;
        } else if (status >= 6 && status <= 8) {
          res = USER.FS_VIEW_6;
        } else if (status >= 9 && status <= 10) {
          res = USER.FS_VIEW_8;
        }
      }
      return res;
    }),
  },

  create: {

    getModel() {
      let model = this.store.createRecord(get(this, 'modelName'));

      // prepare model defaults
      model.set('participation_local_currency', 'EUR');

      return this.store.findAll('project').then((projects) => {
        let cityId = ENV.APP.default_city || null;

        if (cityId) {
          return this.store.findRecord('city', cityId).then((city) => {
            let defaults = { departure_point: city, accommodation_local_currency: 'EUR' };
            let travel = this.store.createRecord('travel-info', defaults);

            model.get('travel_info').addObject(travel);

            return model;
          }).catch(() => {
            // in case the cityId does not exist
            return model;
          });
        } else {
          return model;
        }
      });
    },

    fieldsets: computed('role', function() {
      let role = get(this, 'role');
      let res = [{}];

      if (role === 'MANAGER') {
        res = USER.FS_CREATE_1;
      }

      return res;
    }),
  },

  edit: {
    onSubmit(model) {
      // If after editing, a new application-item instance is returned,
      // which is the case for some status changes, redirect to new instance
      let new_id = model.get('new_id');
      if (new_id) {
        this.transitionTo('application-item.record.edit.index', new_id);
      } else {
        this.refresh();
      }
    },
    fieldsets: computed('role', 'model.status', function() {
      let role = get(this, 'role');
      let status = this.get('model.status');
      let res = [{}];

      if (role === 'MANAGER') {
        if (status < 5) {
          res = USER.FS_EDIT_1;
        } else if (status >= 5) {
          res = USER.FS_EDIT_6;
        }
      }

      return res;
    }),
  },
});
