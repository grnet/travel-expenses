import Ember from 'ember';
import BaseField from './model-form/fields/base';

const {
  get,
  set,
  isArray,
  assign,
  computed,
  computed: { alias, equal, gt, reads } 
} = Ember;

const DEFAULTS = {
  means_of_transport: "AIR",
  meals: "NON",
  participation_local_currency: "EUR",
  accommodation_local_currency: "EUR"
}

function newRecord(arr) {
  let index = arr.get('length') + 1;
  let props = assign({}, DEFAULTS, {index});
  let prev = arr.objectAt(index - 2);
  if (prev) {
    set(props, 'departure_point', get(prev, 'arrival_point'));
    set(props, 'depart_date', get(prev, 'return_date'));
  }
  return arr.createRecord(props);
}

export default Ember.Component.extend(BaseField, {

  loading: true,
  activeIndex: 0,

  uiToDisplay: computed('account.user.user_group', function() {

    let group = this.get('account.user.user_group');
    let ui = '';

    if ( group == 'USER' ) {
      ui = 'user';
    } else if ( group == 'MANAGER') {
      ui = 'manager';
    } else if ( group == 'SECRETARY') {
      ui = 'secretary';
    } else if ( group == 'CONTROLLER') {
      ui = 'controller';
    }
    return ui;
  }),

  activeTravelInfo: computed('travelInfos.[]', 'activeIndex', function() {
    let infos = this.get('travelInfos');
    let info = infos.objectAt(this.get('activeIndex'));
    return info;
  }),

  travelInfos: reads('value'),
  loading: reads('travelInfos.isPending'),

  init() {
    this.get('value').then((result) => {
      if (!result.length) { newRecord(result); }
    });
    this._super(...arguments);
  },

  actions: {
    showInfo(index) {
      set(this, 'activeIndex', index);
    },

    confirmRemove(index) {
      let travelInfos = get(this, 'travelInfos');
      if (index === undefined) {
        index = travelInfos.get('length') - 1;
      }
      if (travelInfos.get('length') > 1) {
        travelInfos.removeAt(index);
      }
    },

    add() {
      let infos = get(this, 'travelInfos');
      let model = newRecord(infos);
      set(this, 'activeIndex', get(infos, 'length') - 1);
    }
  }
});
