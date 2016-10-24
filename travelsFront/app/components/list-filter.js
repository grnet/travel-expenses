import Ember from 'ember';

export default Ember.Component.extend({

	store: Ember.inject.service(),
	i18n: Ember.inject.service(),
	
  classNames: ['list-filter'],
  valueName: '',
  valueProject: '',
  valueStartDate: '',
  valueEndDate: '',
  placeholderLabel: '',
  projects: Ember.computed('project', function(){
  	var store = this.get('store');
  	return store.findAll('project');
  }),

  init() {
    this._super(...arguments);
    this.set('results', this.get('model'));
    this.set('placeholderLabel', this.get('i18n').t('paceholder.filterByProject'));
  },

  actions: {
  	handleChange(project){
  		this.set('valueProject', project);
  		this.set('placeholderLabel', '');
  	},

    handleFilterEntry() {
      let filterInputValueName = this.get('valueName');
      let filterInputValueProject = this.get('valueProject.id');
      let filterInputValueStartDate = this.get('valueStartDate');
      let filterInputValueEndDate = this.get('valueEndDate');
      console.log("This is project id ", filterInputValueProject);
      let filterAction = this.get('filter');

      filterAction(filterInputValueName, filterInputValueProject, filterInputValueStartDate, filterInputValueEndDate).then((filterResults) => this.set('results', filterResults));
    },

    clearFilters() {
    	let filterInputValueName = this.set('valueName', '');
    	let filterInputValueProject = this.set('valueProject', '');
    	let filterInputValueStartDate = this.set('valueStartDate', '');
      let filterInputValueEndDate = this.set('valueEndDate', '');
      this.set('placeholderLabel', this.get('i18n').t('paceholder.filterByProject'));
    	let filterAction = this.get('filter');
    	filterAction(filterInputValueName).then((filterResults) => this.set('results', filterResults));
    }
  }

});

