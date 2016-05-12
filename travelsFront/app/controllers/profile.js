import Ember from 'ember';

export default Ember.Controller.extend({

	profileMessage:'',

	actions: {

		profileUpdate(){
			let profileIsValid=this.get('model.validations.isValid')

			// console.log(this.get('models.validations.attrs.username.messages'))
			if (profileIsValid) {

				var self=this;
				this.get('model').save().then(function(value) {
					self.set('profileMessage','Τα στοιχεία του προφίλ σας έχουν αποθηκευθεί επιτυχώς !');
					Ember.$('#divMessage').addClass('greenMessage');

				}, function(reason) {
					self.set('profileMessage','Η αποθήκευση των στοιχείων του προφίλ σας απέτυχε...');
					Ember.$('#divMessage').addClass('redMessage');

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

		},
		setCategory(id){
			var rec = this.store.peekRecord('category', id);
			this.get('model').set('category', rec);

		}

	},


});
