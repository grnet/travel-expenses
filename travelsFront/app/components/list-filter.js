import Ember from 'ember';
import { translationMacro as t } from "ember-i18n";
import ENV from 'travels-front/config/environment'; 

const CHOICES = ENV.APP.resource_choices;

const {
  on, assign
} = Ember;

export default Ember.Component.extend({

	store: Ember.inject.service(),
	
  classNames: ['list-filter'],
  filters: {dse: '', name: '', project: '',status: '', startDate: '', endDate: ''},
  placeholderLabel: t('placeholder.filterByProject'),
  projects: Ember.computed(function(){
  	var store = this.get('store');
  	return store.findAll('project');
  }),


  actions: {

    handleFilterEntry() {
      this.updateFilters(assign({}, this.get('filters')));
    },

    clearFilters() {
      this.updateFilters({});
    }
  }
});

