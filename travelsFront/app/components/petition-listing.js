import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Component.extend({
	
	deleteMessage: "",
	statePetitionList: "",
  tagName: 'tr',

	actions: {

		edit(id, status) {
			if (status == 1){
				this.sendAction('edit', id);
			}
		},

		del(id, status) {
			if (status == 1){
				this.sendAction('del', id);
			}
		},

		undo(id, status) {
			if (status == 2){
				this.sendAction('undo', id);
			}
		},
	}
});
