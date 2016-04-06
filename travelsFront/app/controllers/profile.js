import Ember from 'ember';

export default Ember.Controller.extend({

	actions: {
		
		profileUpdate(){
			console.log('My username is: ', this.get('username'));
			console.log('My password is: ', this.get('password'));
			console.log('My email is: ', this.get('email'));
			

			var profile = this.store.createRecord('profile',{
					type: 'profile',
					id: this.get('taxRegNum'), //the id will have to change
					first_name: this.get('first_name'),
					last_name: this.get('last_name'),
					iban: this.get('iban'),
					specialtyID: this.get('specialtyID'),
					userKind: this.get('userKind'),
					taxRegNum: this.get('taxRegNum'),
					taxOffice: this.get('taxOffice')
					
				
			});


			profile.save();
			
		}
	}
});
