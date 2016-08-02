import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Component.extend({
	
	deleteMessage: "",
	statePetitionList: "",
  tagName: 'tr',

	actions: {

		// petitionDelete(id,status){
		// 	var self=this;
		// 	var store = this.get('targetObject.store');

		// 	if (status == 1){
		// 			store.findRecord('user-petition', id).then(function(petition) {
		// 			petition.destroyRecord().then(function() {

		// 				self.set('statePetitionList', true);
		// 				self.set('deleteMessage', "Η αίτηση σας έχει διαγραφεί επιτυχώς !");
		// 			}, function(reason) {
		// 				self.set('statePetitionList', false);
		// 				self.set('deleteMessage', 'Η διαγραφή της αίτησης σας απέτυχε...');
		// 			}); 
		// 		});	
		// 	}
		// 	else{
		// 		self.set('statePetitionList', false);
		// 		self.set('deleteMessage', 'Η αίτηση σας έχει υποβληθεί συνεπώς δεν είναι δυνατή η διαγραφή της...');
		// 	}
		// },

		del(id,status) {
			if (status == 1){
				this.sendAction('del', id);
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
