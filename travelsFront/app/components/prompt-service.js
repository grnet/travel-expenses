import Ember from 'ember';

const {
  inject,
  on,
  get,
  set,
  assert
} =  Ember;

export default Ember.Component.extend({
  tagName: '',
  service: inject.service('prompt'),
  initService: on('init', function() {
    let component = get(this, 'service.component');
    assert('component already registered to service', !component);
    this.get('service').set('component', this);
  }),
  visible: false,
  fullscreen: true,
  action: function() {},
  actions: {
    handleClose() {
      set(this, 'visible', false);
    },

    handleConfirm() {
      let action = get(this, 'action');
      if (action) {
        action();
        set(this, 'visible', false);
      }
    }
  }
});
