import Ember from 'ember';

const {
  get, set, merge
} = Ember;


const DEFAULTS = {
  promptTitle: 'Are you sure?',
  promptMessage: '',
  confirmLabel: 'OK',
  cancelLabel: 'Cancel',
};

export default Ember.Service.extend({
  DEFAULTS,
  component: null,
  showPrompt(options) {
    options = merge({}, options || {});
    options = merge(DEFAULTS, options);

    let component = get(this, 'component');

    Object.keys(options).forEach((key) => {
      set(component, key, options[key]);
    })
    
    component.set('visible', true);
  }
});
