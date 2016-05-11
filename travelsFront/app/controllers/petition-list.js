import Ember from 'ember';

export default Ember.Controller.extend({

	deleteMessage: "",
	statePetitionList: "",
	
	actions: {

		petitionDelete(id,status){

			var self=this;
			
			if (status === "δημιουργηθείσα από μετακινούμενο"){

				self.store.findRecord('petition', id).then(function(petition) {
					
					petition.destroyRecord().then(function(value) {
						self.set('statePetitionList', true);
						self.set('deleteMessage', "Η αίτηση σας με id: " + value.id + " έχει διαγραφεί επιτυχώς !");
						Ember.$('#divMessage').removeClass('redMessage');
						Ember.$('#divMessage').addClass('greenMessage');
						console.log(value.id.name);
						

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
			this.transitionToRoute('editPetition',id);
		}

	}

});
