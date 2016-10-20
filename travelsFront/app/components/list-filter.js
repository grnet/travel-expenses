import Ember from 'ember';

export default Ember.Component.extend({

	store: Ember.inject.service(),
	i18n: Ember.inject.service(),
	
  classNames: ['list-filter'],
  value_name: '',
  value_project: '',
  value_startDate: '',
  value_endDate: '',
  placeholder_message: '',
  projects: Ember.computed('project', function(){
  	var store = this.get('store');
  	return store.findAll('project');
  }),

  init() {
    this._super(...arguments);
    this.set('results', this.get('model'));
    this.set('placeholder_message', this.get('i18n').t('paceholder.filterByProject'));
  },

  actions: {
  	handleChange(project){
  		this.set('value_project', project);
  		this.set('placeholder_message', '');
  	},

    handleFilterEntry() {
      let filterInputValueName = this.get('value_name');
      let filterInputValueProject = this.get('value_project.id');
      let filterInputValueStartDate = this.get('value_startDate');
      let filterInputValueEndDate = this.get('value_endDate');
      console.log("This is project id ", filterInputValueProject);
      let filterAction = this.get('filter');

      filterAction(filterInputValueName, filterInputValueProject, filterInputValueStartDate, filterInputValueEndDate).then((filterResults) => this.set('results', filterResults));
    },

    clearFilters() {
    	let filterInputValueName = this.set('value_name', '');
    	let filterInputValueProject = this.set('value_project', '');
    	let filterInputValueStartDate = this.set('value_startDate', '');
      let filterInputValueEndDate = this.set('value_endDate', '');
      this.set('placeholder_message', this.get('i18n').t('paceholder.filterByProject'));
    	let filterAction = this.get('filter');
    	filterAction(filterInputValueName).then((filterResults) => this.set('results', filterResults));
    }
  }

});

