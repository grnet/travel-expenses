import Ember from 'ember';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import meta from 'travel/lib/meta';
import moment from 'moment';
import ENV from 'travel/config/environment';
import { applicationActions } from '../utils/common/actions';

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
    fieldsets: [{
      label: 'personal_info.label',
      fields: [
        'first_name',
        'last_name',
        'specialty',
        'kind',
        'tax_reg_num',
        'tax_office.name',
        'iban',
        'user_category',
      ],
      layout: {
        flex: [50, 50, 50, 50, 50, 50, 50,50]
      }
    },
    {
      label: 'application.label',
      fields: [
        'dse',
        'project.name',
        'reason',
        'task_start_date_time_format',
        'task_end_date_time_format',
        meta.forms.travel_info,
        'participation_local_cost',
        'participation_local_currency',
        'user_recommendation',
        'status_label',
      ],
      layout: {
        flex: [50, 50, 100, 50, 50, 100, 50, 50, 100, 100]
      }
    }],
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

    fieldsets: [{
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
    }],
  },

  edit: {
    fieldsets: [{
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
    }],
  },
});
