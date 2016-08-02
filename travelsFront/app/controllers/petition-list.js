import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Controller.extend({

	deleteMessage: "",
	statePetitionList: "",

	actions: {

		petitionDelete(id,status){

			var self=this;
			var model=this.get('model');
				
				self.store.findRecord('user-petition', id).then(function(petition) {
					petition.destroyRecord().then(function() {
						self.set('statePetitionList', true);
						self.set('deleteMessage', "Η αίτηση σας έχει διαγραφεί επιτυχώς !");	
					}, function(reason) {
						self.set('statePetitionList', false);
						self.set('deleteMessage', 'Η διαγραφή της αίτησης σας απέτυχε...');
					}); 
				});	
		},

		petitionUndo(id){
			var self=this;
			var model=this.get('model');
			var petition=self.store.peekRecord('petition',id);

			self.store.findRecord('petition-status',ENV.petition_status_1).then(function(status){
				petition.set('status',status);
				petition.save();
			});
		},	
	}

});
