import Ember from 'ember';
import { translationMacro as t } from "ember-i18n";

export default Ember.Component.extend({

	store: Ember.inject.service(),
	
  classNames: ['list-filter'],
  filters: {name: '', project: '', startDate: '', endDate: ''},
  placeholderLabel: t('placeholder.filterByProject'),
  projects: Ember.computed(function(){
  	var store = this.get('store');
  	return store.findAll('project');
  }),
  

  actions: {

  	handleChange(project){
      this.set('filters.project', project);
  	},

    handleFilterEntry() {

      let filterInputValue = {
        name: this.get('filters.name'),
        project: this.get('filters.project.id'),
        startDate: this.get('filters.startDate'),
        endDate: this.get('filters.endDate')
      };

      let filterAction = this.get('filter');
      filterAction(filterInputValue).then((filterResults) => this.set('results', filterResults));
    },

    clearFilters() {

      let filterInputValue = {
        name: this.set('filters.name', ''),
        project: this.set('filters.project', ''),
        startDate: this.set('date', null),
        endDate: this.set('date', null)
      };

    	let filterAction = this.get('filter');
      filterAction(filterInputValue).then((filterResults) => this.set('results', filterResults));
    }
  }
});

