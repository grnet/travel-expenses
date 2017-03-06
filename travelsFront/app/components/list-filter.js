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
  filters: {dse: '', last_name: '', project: '', status: '', depart_date__gte: '', return_date__lte: ''},
  placeholderLabel: t('placeholder.filterByProject'),
  placeholderLabelS: t('placeholder.filterByStatus'),
  statuses: Ember.computed(function(){
    var status = CHOICES.STATUS;
    var statusLabel = [];
    for (var i=0; i < status.length; i++ ){
      statusLabel[i] = status[i][0] + ":" + status[i][1]; 
    }
    return statusLabel;
  }),  
  projects: Ember.computed(function(){
  	var store = this.get('store');
  	return store.findAll('project');
  }),


  actions: {

    handleFilterEntry() {
      this.updateFilters(assign({}, this.get('filters')));
    },

    clearFilters() {
      let emptyFilters = {
        dse: this.set('filters.dse', ''),
        last_name: this.set('filters.last_name', ''),
        project: this.set('filters.project', ''),
        status: this.set('filters.status', ''),
        status: this.set('filters.status', ''),
        depart_date__gte: this.set('depart_date__gte', null),
        return_date__lte: this.set('return_date__lte', null)
      };
      this.updateFilters(emptyFilters);
    }
  }
});

