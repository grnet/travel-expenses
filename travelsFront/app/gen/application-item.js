import Ember from 'ember';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import meta from 'travel/lib/meta';
import moment from 'moment';
import ENV from 'travel/config/environment';
import { applicationActions } from '../utils/common/actions';
import PROFILE from '../utils/common/profile';
import USER from '../utils/application/user';

const {
  get,
  computed,
  computed: { reads },
} = Ember;


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

  common: {
    preloadModels: [ 'city' ]
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
      actions: ['gen:details', 'gen:edit', 'submit', 'undo'],
      actionsMap: {
        submit: applicationActions.submit,
        undo: applicationActions.undo,
      }
    }
  },

  details: {
    fieldsets: computed('role', function() {
      let role = get(this, 'role');
      let res = [];
      if (role === 'USER' || role === 'MANAGER') {
        res = [PROFILE.FS_DETAILS, USER.FS_VIEW_1]
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
            let defaults = { departure_point: city }
            let travel = this.store.createRecord('travel-info', defaults)
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
        res = [ USER.FS_CREATE_1 ]
      }
      return res;
    }),
  },

  edit: {
  fieldsets: computed('role', function() {
    let role = get(this, 'role');
    let res = [];
    if (role === 'USER' || role === 'MANAGER') {
      res = [ USER.FS_EDIT_1 ]
    }
    return res;
  }),
  },
});
