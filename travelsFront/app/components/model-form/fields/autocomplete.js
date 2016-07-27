import Ember from 'ember';
import Select from './select';
import _ from 'lodash/lodash';

const {
  get,
  set,
  isArray,
  computed,
  computed: { alias, equal },
  observer
} = Ember;

export default Select.extend({
  init() {
    this._super();
  },
  choiceModel: computed('value', function() {
    let value = get(this, 'value');
    if (!value) { return null; }
    return {label: value.get('name'), value: value};
  }),

  observeChoice: observer('choiceModel', function() {
    let model = this.get('choiceModel');
    if (!model) { return; }
    this.sendAction('onChange', this.get('choiceModel').value);
  })
}) 
