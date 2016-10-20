import Ember from 'ember';

export default Ember.Component.extend({
  classNames: ['list-filter'],
  value_name: '',

  init() {
    this._super(...arguments);
    this.set('results', this.get('model'));
  },

  actions: {
    handleFilterEntry() {
      let filterInputValueName = this.get('value_name');
      let filterAction = this.get('filter');

      filterAction(filterInputValueName).then((filterResults) => this.set('results', filterResults));
    },

    clearFilters() {
    	let filterInputValueName = this.set('value_name', '');
    	let filterAction = this.get('filter');
    	filterAction(filterInputValueName).then((filterResults) => this.set('results', filterResults));
    }
  }

});

