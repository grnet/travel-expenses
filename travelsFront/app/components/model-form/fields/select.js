import Ember from 'ember';
import BaseField from './base';
import _ from 'lodash/lodash';

const {
  get,
  set,
  isArray,
  computed,
  computed: { alias, equal } 
} = Ember;


export default Ember.Component.extend(BaseField, {

  disabled: computed('fattrs.readonly', 'fatrrs.disabled', function() {
    return get(this, 'fattrs.readonly') || get(this, 'fattrs.disabled');
  }),

  isRelation: equal('field.type', 'relation'),

  choicesValues: computed('field.choices.[]', 'isRelation', function() {
    let choices = get(this, 'field.choices') || {};
    if (isArray(choices)) {
      return choices.map((k) => k[0]);
    }
    choices = get(this, 'choicesMap');
    return Object.keys(choices).map((k) => k);
  }),

  choicesMap: computed('field.choices.[]', function() {
    let choices = get(this, 'field.choices');
    if (!isArray(choices)) {
      return choices || {};
    }
    let keys = choices.map((k) => k[0]);
    let values = choices.map((k) => k[1]);
    return _.object(keys, values);
  }),

  relatedChoices: computed('field.relModel', function() {
    let arr = get(this, 'store').findAll(get(this, 'field.relModel'));
    let labelAttr = get(this, 'fattrs.labelKey') || 'name';

    // TODO: convert to promise
    return arr.then(function(results) {
      return Ember.ArrayProxy.create({
        content: arr,
        objectAtContent: function(idx) {
          let item = get(this, 'content').objectAt(idx);
          return { value: item, label: item.get(labelAttr) };
        }
      });
    });
  }),

  choices: computed('choicesValues.[]', 'isRelation', function() {
    let relation = get(this, 'isRelation');
    if (relation) {
      return get(this, 'relatedChoices');
    }

    let choices = get(this, 'choicesValues');
    let map = get(this, 'choicesMap');
    return choices.map((val) => {
      return {
        label: map[val], value: val
      };
    });
  }),

  getChoicesCBPromise: computed('choices.[]', function() {
    let choices = get(this, 'choices');
    return function() {
      return new Ember.RSVP.Promise(function(resolve){
        resolve(choices);
      }.bind(this));
    }
  }),

  getChoicesCB: computed('choices.[]', function() {
    return function() {
      return get(this, 'choices');
    }.bind(this);
  }),

  getChoiceLabel: computed(function() {
    let labelAttr = get(this, 'fattrs.labelKey') || 'name';
    let relation = get(this, 'isRelation');
    if (relation) {
      return function(item) {
        return item.get(labelAttr);
      }
    };

    let choices = get(this, 'choicesMap');
    return function(item) {
      if (item in choices) { return choices[item]; }
      if (_.isString(item)) { return item; }
      return item.label;
    }
  })
});
