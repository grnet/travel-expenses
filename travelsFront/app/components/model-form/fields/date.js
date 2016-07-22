import PaperInput from 'ember-paper/components/paper-input';
import Ember from 'ember';
import BaseField from './base';

const { get, computed, computed: { alias } } = Ember;

export default PaperInput.extend(BaseField, {
  tagName: 'md-input-container',

  dateValue: alias('value'),

  handleDate(val) {
    this.sendAction('onChange', val);
  },

  setValue() {}
});
