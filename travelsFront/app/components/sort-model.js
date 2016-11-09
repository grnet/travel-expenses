import Ember from 'ember';
import Select from './model-form/fields/select';
import _ from 'lodash/lodash';
import ENV from 'travels-front/config/environment'; 

const {
  get,
  set,
  isArray,
  computed,
  computed: { alias, equal },
  observer
} = Ember;

export default Select.extend({
  layoutName: 'components/model-form/fields/select',


  getChoicesCBPromise: computed('choices.[]', function() {

  let choices = get(this, 'choices'); 
  
	  return function() {
	    return new Ember.RSVP.Promise((resolve) => {    	
	      resolve(choices.then((results) => {
	      	var sortedProjects = results.sortBy('label');
	      	return sortedProjects;
	      }));
	    });
	  }
  }),
});
