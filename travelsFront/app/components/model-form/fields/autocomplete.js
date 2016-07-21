import Ember from 'ember';
import Select from './select';
import _ from 'lodash/lodash';

const {
  get,
  set,
  isArray,
  computed,
  computed: { alias, equal } 
} = Ember;

export default Select.extend({
  choiceModel: null
}) 
