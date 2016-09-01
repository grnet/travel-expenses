import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Component.extend({
	
	deleteMessage: "",
	statePetitionList: "",
  tagName: 'tr',

	actions: {

		edit(id, status) {
			if (status == 1 || this.get('account.user.user_group') === "SECRETARY"){
				this.sendAction('edit', id);
			}
		},

		del(id, status) {
			if (status == 1){
				this.sendAction('del', id);
			}
		},

		undo(petition) {
      this.sendAction('undo', petition);
		},
	}
});
