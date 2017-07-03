import Ember from 'ember';
import { translationMacro as t } from "ember-i18n";
import ENV from 'travels-front/config/environment'; 

const CHOICES = ENV.APP.resource_choices;

const {
  on, assign
} = Ember;

export default Ember.Component.extend({

	store: Ember.inject.service(),
	
  filters: {project: ''},
  placeholderLabel: t('placeholder.filterByProject'),
  projects: Ember.computed(function(){
  	var store = this.get('store');
  	return store.findAll('project');
  }),


  actions: {

  	statsExportPerProject() { 
  		var project_id = this.get('filters.project.id');
  		var project_name = this.get('filters.project.name');
      this.sendAction('statsExportPerProject', project_id, project_name);
    },

  	statsExport() {
      this.sendAction('statsExport');
    },
  }
});

