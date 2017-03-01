import Ember from 'ember';
import { translationMacro as t } from "ember-i18n";
import ENV from 'travels-front/config/environment'; 

const CHOICES = ENV.APP.resource_choices;

export default Ember.Component.extend({

	store: Ember.inject.service(),
	
  classNames: ['list-filter'],
  filters: {dse: '', name: '', project: '',status: '', startDate: '', endDate: ''},
  placeholderLabel: t('placeholder.filterByProject'),
  projects: Ember.computed(function(){
  	var store = this.get('store');
  	return store.findAll('project');
  }), 

  placeholderLabelS: t('placeholder.filterByStatus'),
  statuses: Ember.computed(function(){
    var status = CHOICES.STATUS;
    var statusLabel = [];
    for (var i=0; i < status.length; i++ ){
      statusLabel[i] = status[i][0] + ":" + status[i][1]; 
    }
    return statusLabel;
  }), 
  

  actions: {

  	handleChange(project){
      this.set('filters.project', project);
  	}, 

    handleChangeS(status){      
      this.set('filters.status', status);
    }, 
    

    handleFilterEntry() {
      let filterInputValue = {
        dse: this.get('filters.dse'),
        name: this.get('filters.name'),
        project: this.get('filters.project.id'),
        status: this.get('filters.status').substring(0, this.get('filters.status').indexOf(":")),
        startDate: this.get('filters.startDate'),
        endDate: this.get('filters.endDate')
      };

      this.updateFilters(filterInputValue);
    },

    clearFilters() {

      let filterInputValue = {
        dse: this.set('filters.dse', ''),
        name: this.set('filters.name', ''),
        project: this.set('filters.project', ''),
        status: this.set('filters.status', ''),
        startDate: this.set('date', null),
        endDate: this.set('date', null)
      };

      this.updateFilters(filterInputValue);
    }
  }
});

