import Ember from 'ember';

const {
  get,
  set,
  inject
} = Ember;


export default Ember.Component.extend({
  tagName: '',
  promptService: inject.service('prompt'),
  actions: {
    handleClick() {
      let action = get(this, 'action');
      let confirm = get(this, 'confirm');
      let prompt = get(this, 'promptService');

      if (confirm) {
        let options = {};
        let commonAttrs = Object.keys(prompt.DEFAULTS);
        commonAttrs.forEach((key) => {
          let value = get(this, key);
          if (value !== undefined) {
            options[key] = value;
          }
        });
        options.action = action;
        prompt.showPrompt(options);
      } else {
        action();
      }
    }
  }
});
