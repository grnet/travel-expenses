import Ember from 'ember';
import ENV from 'travels-front/config/environment';

export default Ember.Controller.extend({

	deleteMessage: "",
	statePetitionList: "",

	actions: {

		petitionDelete(id,status){

			var self=this;

			if (status === "σε επεξεργασία απο τη γραμματεία" || status === "υποβεβλημένη από μετακινούμενο"){

				self.store.findRecord('petition', id).then(function(petition) {

					petition.destroyRecord().then(function(value) {
						self.set('statePetitionList', true);
						self.set('deleteMessage', "Η αίτηση με id: " + value.id + " έχει διαγραφεί επιτυχώς !");
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
				self.set('deleteMessage', 'Η αίτηση έχει υποβληθεί συνεπώς δεν είναι δυνατή η διαγραφή της...');
				Ember.$('#divMessage').removeClass('greenMessage');
				Ember.$('#divMessage').addClass('redMessage');
			}

		},
		petitionUndo(id){
			var self=this;
			var model=this.get('model');


			var petition=self.store.peekRecord('petition',id);

			self.store.findRecord('petition-status',ENV.petition_status_3).then(function(status){
				petition.set('status',status);
				petition.save();
			});


		},
		petitionEdit(id){
			id=id.substring(id.indexOf('user_petition/')+14,id.lastIndexOf('/'));
			this.transitionToRoute('advancedPetition',id);
		},
		clearMessage(){
			var self=this;
			self.set('deleteMessage','');
		}

	}

});
