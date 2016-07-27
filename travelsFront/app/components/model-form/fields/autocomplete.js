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
  choiceModel: null,
  observeValue: observer('value', function() {
    let value = get(this, 'value');
    let label = get(this, 'value.' + (get(this, 'fattrs.labelKey') || 'name'));
    set(this, 'choiceModel', {
      label,
      value
    })
  }),

  observeChoice: observer('choiceModel', function() {
    let model = this.get('choiceModel');
    this.sendAction('onChange', model && model.value);
  })
}) 
