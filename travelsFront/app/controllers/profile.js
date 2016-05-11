import Ember from 'ember';

export default Ember.Controller.extend({

	profileMessage:'',
	stateProfile:'',

	actions: {

		profileUpdate(){
			let profileIsValid=this.get('model.validations.isValid')

			// console.log(this.get('models.validations.attrs.username.messages'))
			if (profileIsValid) {
				//this.get('model').save();

				var self=this;
				this.get('model').save().then(function(value) {
					self.set('stateProfile', true);
					self.set('profileMessage','Τα στοιχεία του προφίλ σας έχουν αποθηκευθεί επιτυχώς !');

				}, function(reason) {
					self.set('stateProfile', false);
					self.set('profileMessage','Η αποθήκευση των στοιχείων του προφίλ σας απέτυχε...');

				});
			}
		},

		setSpecialty(id){
			var rec = this.store.peekRecord('specialty', id);
			this.get('model').set('specialtyID', rec);

		},

		setKind(id){
			var rec = this.store.peekRecord('kind', id);
			this.get('model').set('kind', rec);

		},
		setTaxOffice(id){
			var rec = this.store.peekRecord('tax-office', id);
			this.get('model').set('taxOffice', rec);

		}

	},


});
