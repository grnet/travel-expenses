import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Component.extend({
	
	deleteMessage: "",
	statePetitionList: "",
  tagName: 'tr',
  promptService: Ember.inject.service('prompt'),

	actions: {

		edit(model) {
			if (model.get('status') == 1 || this.get('account.user.user_group') === "SECRETARY"){
				this.sendAction('edit', model);
			}

		},

		del(model) {
      this.sendAction('del', model);
		},

		undo(model) {
      this.sendAction('undo', model);
		},
	}
});
