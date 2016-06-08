import Ember from 'ember';

export default Ember.Controller.extend({

	deleteMessage: "",
	statePetitionList: "",

	actions: {

		petitionDelete(id,status){

			var self=this;
			var model=this.get('model');

			if (status === "δημιουργηθείσα από μετακινούμενο"){

				self.store.findRecord('petition', id).then(function(petition) {
					petition.destroyRecord().then(function() {
						
						self.set('statePetitionList', true);
						self.set('deleteMessage', "Η αίτηση σας με id: " + id + " έχει διαγραφεί επιτυχώς !");
						Ember.$('#divMessage').removeClass('redMessage');
						Ember.$('#divMessage').addClass('greenMessage');

					}, function(reason) {
						self.set('statePetitionList', false);
						self.set('deleteMessage', 'Η διαγραφή της αίτησης σας απέτυχε...');
						Ember.$('#divMessage').removeClass('greenMessage');
						Ember.$('#divMessage').addClass('redMessage');

					}); 

				});	

			}

			else{
				self.set('statePetitionList', false);
				self.set('deleteMessage', 'Η αίτηση σας έχει υποβληθεί συνεπώς δεν είναι δυνατή η διαγραφή της...');
				Ember.$('#divMessage').removeClass('greenMessage');
				Ember.$('#divMessage').addClass('redMessage');
			}

		},

		petitionEdit(id){
			id=id.substring(id.indexOf('user_petition/')+14,id.lastIndexOf('/'));
			this.transitionToRoute('editPetition',id);
		},
		clearMessage(){
			var self=this;
			self.set('deleteMessage','');
		}

	}

});
