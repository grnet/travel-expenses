import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Component.extend({
	
	deleteMessage: "",
	statePetitionList: "",
  tagName: 'tr',

	actions: {

		del(id, status) {
			if (status == 1){
				this.sendAction('del', id);
			}
		},

		edit(id, status) {
			if (status == 1){
				this.sendAction('edit', id);
			}
		},
	}
});
