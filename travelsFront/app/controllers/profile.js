import Ember from 'ember';

export default Ember.Controller.extend({

	actions: {

		profileUpdate(){
			console.log('Hi there, please authorize me', this.get('model.taxRegNum'));

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

			this.get('model').save();

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
