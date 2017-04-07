import Ember from 'ember';

import ENV from 'travels-front/config/environment'; 

export default Ember.Component.extend({
	
	deleteMessage: "",
	statePetitionList: "",
  tagName: '',
  promptService: Ember.inject.service('prompt'),

	actions: {

		edit(model) {
			this.sendAction('edit', model);
		},

		del(model) {
      this.sendAction('del', model);
		},

		undo(model) {
      this.sendAction('undo', model);
		},

		view(model) {
      this.sendAction('view', model);
		},

		pdf(model, pdf_id) {
      this.sendAction('pdf', model, pdf_id);
		},

		approve(model) {
      this.sendAction('approve', model);
		},

		managerApproval(model) {
      this.sendAction('managerApproval', model);
    },

    managerCostApproval(model) {
      this.sendAction('managerCostApproval', model);
    },
	}
});
