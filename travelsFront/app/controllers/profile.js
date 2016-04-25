import Ember from 'ember';

export default Ember.Controller.extend({

	//currentUser: null,

	//init: function() {
		//this._super();
		//this.get('store').findRecord('profile', 1).then((profile) => {
			//this.set('currentUser', profile);
		//});
		//console.log(this.get('currentUser'))
	//},

	actions: {

		profileUpdate(){

			// var profile = this.store.createRecord('profile',{
			// 		type: 'profile',
			// 		id: this.get('taxRegNum'), //the id will have to change
			// 		first_name: this.get('first_name'),
			// 		last_name: this.get('last_name'),
			// 		iban: this.get('iban'),
			// 		specialty: this.get('specialty'),
			// 		userKind: this.get('userKind'),
			// 		taxRegNum: this.get('taxRegNum'),
			// 		taxOffice: this.get('taxOffice')	
			// });

			let profileIsValid=this.get('model.validations.isValid')

			// console.log(this.get('models.validations.attrs.username.messages'))
			if (profileIsValid) {
				//this.get('model').save();

				var self=this;
				this.get('model').save().then(function(value) {

					self.set('message','Τα στοιχεία του προφίλ σας έχουν αποθηκευθεί επιτυχώς !');
				});
			}
			// else{
			// 	there we should put a warning message: ("Δεν έχετε συμπληρώσει όλα τα 
			//  στοιχεία του προφίλ. Μπορείτε να σώσετε τα υπάρχοντα στοιχεία αλλά 
			//  παρακαλούμε επιστρέψτε σύντομα για να ολοκληρώσετε τη διαδικασία");
			// }
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
