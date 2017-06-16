import Ember from 'ember';
import BaseField from './model-form/fields/base';

const {
  get,
  set,
  isArray,
  assign,
  computed,
  computed: { alias, equal, gt } 
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
  travelInfos: [],
  loading: true,
  activeTravelInfo: null,

  init() {
    this.get('value').then((result) => {
      set(this, 'travelInfos', result);
      set(this, 'loading', false);
      if (result.length) {
        set(this, 'activeTravelInfo', result.objectAt(0));
      } else {
        set(this, 'activeTravelInfo', newRecord(result));
      }
    });
    this._super(...arguments);
  },
  
  actions: {
    showInfo(index) {
      set(this, 'activeTravelInfo', get(this, 'travelInfos').objectAt(index));
    },

    confirmRemove(index) {
      let confirm = window.conrim("Are you sure?");
      if (!confrim) { return; }

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
      set(this, 'activeTravelInfo', model);
    }
  }
});
