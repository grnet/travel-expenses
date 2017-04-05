import gen from 'ember-gen/lib/gen';

const {
  get, computed
} = Ember;

export default gen.CRUDGen.extend({
  modelName: 'user-petition',
  menu: {
    display: true,
  },

  getModel() {
    return get(this, 'store').findRecord('user-petition', 1);
  }
});
