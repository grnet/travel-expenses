import Ember from 'ember';

export default Ember.Controller.extend({

	actions: {
		
		signup(){
			console.log('My username is: ', this.get('username'));
			console.log('My password is: ', this.get('password'));
			console.log('My email is: ', this.get('email'));
			

			this.store.createRecord('user',{
					type: 'user',
					username: this.get('username'),
					password: this.get('password'),
					email: this.get('email')
				
			});
			
		}
	}
});
