import Ember from 'ember';
import gen from 'ember-gen/lib/gen';
import { field } from 'ember-gen';
import ENV from 'travel/config/environment';
import { applicationActions } from '../utils/common/actions';
import USER from '../utils/application/user';
import SECRETARY from '../utils/application/secretary';
import CONTROLLER from '../utils/application/controller';
import VIEWER from '../utils/application/viewer';
import PRESIDENT_SECRETARY from '../utils/application/president-secretary';
import HELPDESK from '../utils/application/helpdesk';
import {abilityStates} from 'travel/lib/application/abilityStates';
import moment from 'moment';

const {
  get,
  computed,
  inject,
  computed: { reads },
} = Ember;

const CHOICES = ENV.APP.resources;


export default gen.CRUDGen.extend({
  order: 200,
  modelName: 'application_item',
  auth: true,
  path: 'applications',
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

      if (role === 'USER' || role === 'MANAGER' || role === 'HELPDESK') {
        val = USER.FS_VALIDATORS;
      } else if (role === 'SECRETARY') {
        val = SECRETARY.FS_VALIDATORS;
      } else if (role === 'CONTROLLER') {
        val = CONTROLLER.FS_VALIDATORS;
      }

      return val;
    }),
  },

  list: {
    routeMixins: [{
      messageService: inject.service('messages'),
      beforeModel(transition) {
        let session = get(this, 'session');
        if (get(session, 'isAuthenticated')) {
          let profile = get(session, 'session.authenticated');
          const PROFILE_PARAMS = ['first_name', 'last_name', 'iban', 'specialty', 'kind', 'tax_reg_num'];
          for (let value of PROFILE_PARAMS) {
            if (profile[value] == null || value == null) {
              transition.abort();
              this.get('messageService').setError('profile.not.complete.error');
              return this.transitionTo('auth.profile');
            };
          }
        }
        return this._super(transition);
      }
    }],
    actions: ['exportStats', 'gen:create'],
    actionsMap: {
      exportStats: applicationActions.exportStats,
    },
    preloadModels: ['project'],
    layout: 'table',
    menu: {
      display: true,
      icon: 'assignment',
      label: computed(function() {
          let session = this.container.lookup('service:session');
          let role = session.get('session.authenticated.user_group');
          if (role === 'SECRETARY' || role === 'CONTROLLER' || role === 'PRESIDENT_SECRETARY' || role === 'VIEWER' || role === 'HELPDESK') {
            return 'applications.list.tab';
          } else if (role === 'MANAGER') {
            return 'applications.list.approve.tab';
          } else if (role === 'USER') {
            return 'my.applications.tab';
          }
      }),
    },
    getModelQueryParams(qs) {
      if (qs && (qs.depart_date__gte || qs.depart_date__lte)) {
        qs.depart_date__gte = moment(qs.depart_date__gte).format("YYYY-MM-DD");
        qs.depart_date__lte = moment(qs.depart_date__lte).format("YYYY-MM-DD");
      }
      return qs
    },
    filter: {
      active: true,
      meta: {
        fields: computed(function() {
          let session = this.container.lookup('service:session');
          let role = session.get('session.authenticated.user_group');
          let res = [];

          if (role === 'SECRETARY' || role === 'CONTROLLER' || role === 'PRESIDENT_SECRETARY' || role === 'VIEWER' || role === 'HELPDESK') {
            res = [
              field('project', { modelName:'project', type: 'model', displayAttr: 'name' }),
              field('status', { type:'select', choices: CHOICES.STATUS }),
              field('depart_date__gte', { type: 'date' }),
              field('depart_date__lte', { type: 'date' }),
            ]
          } else if (role === 'USER' || role === 'MANAGER') {
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
        field('travel_info.firstObject.depart_date_format', { label: 'depart_date_format.label' }),
        field('travel_info.lastObject.return_date_format', { label: 'return_date_format.label' }),
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
    actions: ['submit', 'gen:edit'],
    actionsMap: {
        submit: applicationActions.submit,
    },
    fieldsets: computed('role', function() {
      let role = get(this, 'role');
      let status = this.get('model.status');
      let res = [{}];

      if (role === 'USER' || role === 'MANAGER') {
        if (status >= 1 && status <= 3) {
          res = USER.FS_VIEW_1;
        } else if (status >= 4 && status <= 5) {
          res = USER.FS_VIEW_4;
        } else if (status >= 6 && status <= 8) {
          res = USER.FS_VIEW_6;
        } else if (status >= 9 && status <= 10) {
          res = USER.FS_VIEW_8;
        }
      } else if (role === 'SECRETARY') {
        res = SECRETARY.FS_VIEW_3;
      } else if (role === 'CONTROLLER') {
        res = CONTROLLER.FS_VIEW_8;
      } else if (role === 'VIEWER') {
        res = VIEWER.FS_VIEW;
      } else if (role === 'PRESIDENT_SECRETARY') {
        res = PRESIDENT_SECRETARY.FS_VIEW;
      } else if (role === 'HELPDESK') {
        res = HELPDESK.FS_VIEW;
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
    onSubmit(model) {
      let id = model.get('id');
      if (id) {
        this.transitionTo('application-item.record.index', id);
      } else {
        this.refresh();
      }
    },
    fieldsets: computed('role', function() {
      let role = get(this, 'role');
      let res = [{}];

      if (role === 'USER' || role === 'MANAGER') {
        res = USER.FS_CREATE_1;
      } else if (role === 'HELPDESK') {
        res = HELPDESK.FS_CREATE_1;
      }

      return res;
    }),
  },

  edit: {
    onSubmit(model) {
      // If after editing, a new application-item instance is returned,
      // which is the case for some status changes, redirect to new instance
      let new_id = model.get('new_id');
      let id = model.get('id');
      if (new_id) {
        this.transitionTo('application-item.record.index', new_id);
      } else if (id) {
        this.transitionTo('application-item.record.index', id);
      } else {
        this.refresh();
      }
    },
    fieldsets: computed('role', 'model.status', function() {
      let role = get(this, 'role');
      let status = this.get('model.status');
      let res = [{}];

      if (role === 'USER' || role === 'MANAGER') {
        if (status < 5) {
          res = USER.FS_EDIT_1;
        } else if (status >= 5) {
          res = USER.FS_EDIT_6;
        }
      } else if (role === 'HELPDESK') {
        if (status < 5) {
          res = HELPDESK.FS_EDIT_1;
        } else if (status >= 5) {
          res = HELPDESK.FS_EDIT_6;
        }
      } else if (role === 'SECRETARY') {
        res = SECRETARY.FS_EDIT_3;
      } else if (role === 'CONTROLLER') {
        res = CONTROLLER.FS_EDIT_8;
      }

      return res;
    }),
  },
});
