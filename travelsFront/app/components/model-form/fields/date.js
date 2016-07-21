import PaperInput from 'ember-paper/components/paper-input';
import Ember from 'ember';
import BaseField from './base';

const { get, computed, computed: { alias } } = Ember;

export default PaperInput.extend(BaseField, {
  tagName: 'md-input-container',
  dateValue: computed('value', function() {
    return get(this, 'value') || null;
  }),

  didInsertElement() {
    this._super();
    let input = this.$().find("input");
    input.addClass("md-input");
    let cont = this.$().find(".input-group")
    let icon = this.$().find("md-icon");
    cont.find("span").append(icon).css({
      position: 'absolute', 
      top: 0, 
      right: 15
    });
    cont.css({position: 'relative'});
  },

  handleDate(val) {
    this.sendAction('onChange', val);
  }
});
