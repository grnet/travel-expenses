import Ember from 'ember';
import BaseField from './model-form/fields/base';

const {
  get,
  set,
  isArray,
  computed,
  computed: { alias, equal, gt } 
} = Ember;

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
        set(this, 'activeTravelInfo', result.createRecord());
      }
    });
    this._super(...arguments);
  },
  
  actions: {
    showInfo(index) {
      set(this, 'activeTravelInfo', get(this, 'travelInfos').objectAt(index));
    },

    remove(index) {
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
      let model = infos.createRecord();
      set(this, 'activeTravelInfo', model);
    }
  }
});
