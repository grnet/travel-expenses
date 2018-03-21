import Ember from 'ember';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import meta from 'travel/lib/meta';
import moment from 'moment';
import ENV from 'travel/config/environment';
import { applicationActions } from '../utils/common/actions';
import USER from '../utils/application/user';
import SECRETARY from '../utils/application/secretary';

const {
  get,
  computed,
  computed: { reads },
} = Ember;

const CHOICES = ENV.APP.resources;

const STATUS_MAP = {
  'SAVED_BY_USER': 1,
  'SUBMITTED_BY_USER': 2,
  'SAVED_BY_SECRETARY': 3,
  'SUBMITTED_BY_SECRETARY': 4,
  'APPROVED_BY_PRESIDENT': 5,
  'USER_COMPENSATION': 6,
  'USER_COMPENSATION_SUBMISSION': 7,
  'SECRETARY_COMPENSATION': 8,
  'SECRETARY_COMPENSATION_SUBMISSION': 9,
  'PETITION_FINAL_APPOVAL': 10,
}


export default gen.CRUDGen.extend({
  order: 200,
  modelName: 'application_item',
  auth: true,
  path: 'applications',
  resourceName: 'applications',
  _metaMixin: {
    session: Ember.inject.service(),
    role: reads('session.session.authenticated.user_group')
  },

  abilityStates: {
    usersaved: computed('model.status', function() {
      let status = this.get('model.status');
        return status === STATUS_MAP["SAVED_BY_USER"];
    }),
    usersubmitted: computed('model.status', function() {
      let status = this.get('model.status');
        return status === STATUS_MAP["SUBMITTED_BY_USER"];
    }),
    secretarysaved: computed('model.status', function() {
      let status = this.get('model.status');
        return status === STATUS_MAP["SAVED_BY_SECRETARY"];
    }),
  },

  common: {
    preloadModels: ['city'],
    validators: computed('role', function() {
      let role = get(this, 'role');
      let val = {};
      if (role === 'USER') {
        val = USER.FS_VALIDATORS;
      } else if (role === 'SECRETARY') {
        val = SECRETARY.FS_VALIDATORS;
      }
      return val;
    }),
  },

  list: {
    preloadModels: ['project'],
    layout: 'table',
    menu: {
      display: true,
      icon: 'description',
      label: 'appications_list.tab',
    },
    filter: {
      active: true,
      meta: {
        fields: [
          field('dse', {type: 'text'}),
          field('project', {modelName:'project', type: 'model', displayAttr: 'name'}),
          field('status', {type:'select', choices: CHOICES.STATUS})
        ]
      },
      serverSide: true,
      search: true,
      searchFields: ['dse', 'last_name']
    },
    sort: {
      active: true,
      serverSide: true,
      fields: ['dse']
    },
    paginate: {
      limits: [ 10, 50],
      serverSide: true,
      active: true
    },
    row: {
      fields: [
        'dse',
        'first_name',
        'last_name',
        'project.name',
        'task_start_date_format',
        'task_end_date_format',
        'status_label',
      ],
      actions: ['gen:details', 'gen:edit', 'submit', 'undo', 'pdf', 'approve'],
      actionsMap: {
        submit: applicationActions.submit,
        undo: applicationActions.undo,
        pdf: applicationActions.pdf,
        approve: applicationActions.approve,
      }
    }
  },

  details: {
    fieldsets: computed('role', function() {
      let role = get(this, 'role');
      let res = [];
      if (role === 'USER' || role === 'MANAGER') {
        res = USER.FS_VIEW_1;
      } else if (role === 'SECRETARY') {
        res = SECRETARY.FS_VIEW_3;
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
      let res = [];
      if (role === 'USER' || role === 'MANAGER') {
        res = USER.FS_CREATE_1;
      }
      return res;
    }),
  },

  edit: {
    onSubmit(model) {
      this.transitionTo('application-item.index')
    },
    fieldsets: computed('role', function() {
      let role = get(this, 'role');
      let res = [];
      if (role === 'USER' || role === 'MANAGER') {
        res = USER.FS_EDIT_1;
      } else if (role === 'SECRETARY') {
        res = SECRETARY.FS_EDIT_3;
      }
      return res;
    }),
  },
});
