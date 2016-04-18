import Ember from 'ember';


export default Ember.Controller.extend({

	message:null,

	actions: {

		signup(){
			console.log('My username is: ', this.get('username'));
			console.log('My password is: ', this.get('password'));
			console.log('My email is: ', this.get('email'));

			this.set('uname',this.get('username'));
			this.set('pass',this.get('password'));
			this.set('mail',this.get('email'));
			

			var account = this.store.createRecord('account',{
				type: 'account',
				id: this.get('username'),
				username: this.get('username'),
				password: this.get('password'),
				email: this.get('email')

			});

			this.set('model',account)
			const { m, validations } =this.get('model').validateSync();

			let accountIsValid=validations.get('isValid');
			
			console.log('Account object is:'+accountIsValid);
			if (accountIsValid) {
				account.save();
				this.set('message','Please check the given e-mail for account activation details')


			}
			else{
				console.log("Account is invalid");
			}


		}
	}
});
