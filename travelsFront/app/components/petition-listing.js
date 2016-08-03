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

		petitionUndo(id){
			var self=this;
			var model=this.get('model');
			var petition=self.store.peekRecord('user-petition',id);

			self.store.findRecord('petition-status',ENV.petition_status_1).then(function(status){
				petition.set('status',status);
				petition.save();
			});
		},
	}
});
