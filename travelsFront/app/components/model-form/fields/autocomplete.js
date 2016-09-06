import Ember from 'ember';
import Select from './select';
import _ from 'lodash/lodash';
import slugify from 'travels-front/lib/slugify';

const {
  get,
  set,
  isArray,
  computed,
  computed: { alias, equal },
  observer,
  isPresent,
  assert
} = Ember;

function isString(item) {
  return typeof item === 'string' || item instanceof String;
}

export default Select.extend({
  init() {
    this._super();
    this.updateValue();
  },
  choiceModel: null,
  observeValue: observer('value', function() {
    this.updateValue();
  }),

  updateValue() {
    let value = get(this, 'value');
    if (!value) { return; }
    let label = get(this, 'value.' + (get(this, 'fattrs.labelKey') || 'name'));
    set(this, 'choiceModel', {
      label,
      value
    })
  },

  filterArray(array, searchText, lookupKey) {
    return array.filter(function(item) {
      assert(`You have not defined \`lookupKey\` on paper-autocomplete, when source contained
        items that are not of type String. To fix this error provide a
        lookupKey=\`key to lookup from source item\`.`, isString(item) || isPresent(lookupKey));

      assert(`You specified \`lookupKey\` as a lookupKey on paper-autocomplete,
        but at least one of its values is not of type String. To fix this error make sure that every \`lookupKey\`
        value is a string.`, isString(item) || (isPresent(lookupKey) && isString(get(item, lookupKey))));

      let search = isString(item) ? item.toLowerCase() : get(item, lookupKey).toLowerCase();
      searchText = slugify(searchText);
      search = slugify(search);
      return search.indexOf(searchText) > -1;
    });
  },

  observeChoice: observer('choiceModel', function() {
    let model = this.get('choiceModel');
    this.sendAction('onChange', model && model.value);
  })
}) 
