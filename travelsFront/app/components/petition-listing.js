import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Component.extend({
	
	deleteMessage: "",
	statePetitionList: "",

	actions: {

		petitionDelete(id,status){
			var self=this;
			var model=this.get('model');
			var store = this.get('targetObject.store');

			if (status == 1){
					store.findRecord('petition', id).then(function(petition) {
					petition.destroyRecord().then(function() {

						self.set('statePetitionList', true);
						self.set('deleteMessage', "Η αίτηση σας έχει διαγραφεί επιτυχώς !");
						Ember.$('#messageModal').modal();
						Ember.$('#styleModal').removeClass('btn-warning');
						Ember.$('#styleModal').addClass('btn-success');
						

					}, function(reason) {
						self.set('statePetitionList', false);
						self.set('deleteMessage', 'Η διαγραφή της αίτησης σας απέτυχε...');
						Ember.$('#messageModal').modal();
						Ember.$('#styleModal').removeClass('btn-success');
						Ember.$('#styleModal').addClass('btn-warning');

					}); 

				});	

			}

			else{
				self.set('statePetitionList', false);
				self.set('deleteMessage', 'Η αίτηση σας έχει υποβληθεί συνεπώς δεν είναι δυνατή η διαγραφή της...');
				Ember.$('#messageModal').modal();
				Ember.$('#styleModal').removeClass('btn-success');
				Ember.$('#styleModal').addClass('btn-warning');
			}

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
