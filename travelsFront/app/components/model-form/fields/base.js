import Ember from 'ember';

const { set, computed, computed: { alias } } = Ember;

export default Ember.Mixin.create({
  tagName: '',
  store: Ember.inject.service('store'),
  fattrs: alias('field.attrs'),
  actions: {
    handleChange(value) {
      this.sendAction('onChange', value);
    }
  }
});
