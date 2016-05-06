import Ember from 'ember';

export default Ember.Controller.extend({
	deleteMessage: null,
	actions: {

		petitionDelete(id,status){
			var self =this;
			if (status === "δημιουργηθείσα από μετακινούμενο"){

				self.store.findRecord('petition', id).then(function(petition) {
					petition.destroyRecord().then(function(value) {
						self.set('deleteMessage', "Η αίτηση σας έχει διαγραφεί επιυχώς !")
					}, function(reason) {
						self.set('deleteMessage', 'Η διαγραφή της αίτησης σας απέτυχε...');

					}); 
				});
			}
			else{
				self.set('deleteMessage', 'Η αίτηση σας έχει υποβληθεί συνεπώς δεν είναι δυνατή η διαγραφή της...');
			}

		},

		petitionEdit(id){
			this.transitionToRoute('editPetition');
		}
	}
});
