import Ember from 'ember';

export default Ember.Controller.extend({

	actions: {
		
		signup(){
			console.log('My username is: ', this.get('username'));
			console.log('My password is: ', this.get('password'));
			console.log('My email is: ', this.get('email'));
			

			var account = this.store.createRecord('account',{
					type: 'account',
					id: this.get('username'),
					username: this.get('username'),
					password: this.get('password'),
					email: this.get('email')
				
			});


			account.save();
			
		}
	}
});
