import Ember from 'ember';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import meta from 'travel/lib/meta';
import moment from 'moment';

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
      label: 'appications_list.tab',
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
      actions: ['gen:details', 'gen:edit'],
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
        'task_start_date_format',
        'task_end_date_format',
        'reason',
        'user_recommendation',
        'status_label',
      ],
      layout: {
        flex: [50, 50, 50, 50, 100, 100, 50]
      }
    }],
  },

  create: {

    getModel() {
      let model = this.store.createRecord(get(this, 'modelName'));
      model.set('task_start_date', moment(new Date()).add(1, 'days').toDate());
      model.set('task_end_date', moment(new Date()).add(2, 'days').toDate());
      return this.store.findAll('project').then((projects) => {
        let defaults = {};
        let travel = this.store.createRecord('travel-info', defaults)
        model.get('travel_info').addObject(travel);
        return model;
      });
    },

    fieldsets: [{
      label: 'application_create.title',
      fields: [
        field('dse', {disabled: true}),
        'project',
        'task_start_date',
        'task_end_date',
        'reason',
        'user_recommendation',
        meta.forms.travel_info
      ],
      layout: {
        flex: [50, 50, 50, 50, 100, 100]
      }
    }],
  },

  edit: {
    fieldsets: [{
      label: 'application_create.title',
      fields: [
        field('dse', {disabled: true}),
        'project',
        'task_start_date',
        'task_end_date',
        'reason',
        'user_recommendation',
        meta.forms.travel_info
      ],
      layout: {
        flex: [50, 50, 50, 50, 100, 100]
      }
    }],
  },
});
