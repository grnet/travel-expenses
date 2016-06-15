import Ember from 'ember';


export default Ember.Controller.extend({

	message:'',
	usernameExists:'',
	emailProblems:'',


	actions: {
		clearUserErrorLabels(){
			this.set('message','');
			this.set('usernameExists','');

		},
		clearEmailErrorLabels(){
			this.set('message','');
			this.set('emailProblems','');

		},


		signup(){
			this.set('uname',this.get('username'));
			this.set('pass',this.get('password'));
			this.set('mail',this.get('email'));


			var account = this.store.createRecord('account',{
				type: 'account',
				username: this.get('username'),
				password: this.get('password'),
				email: this.get('email')

			});

			this.set('model',account)
			const { m, validations } =this.get('model').validateSync();

			let accountIsValid=validations.get('isValid');

			if (accountIsValid) {
				var self=this;
				account.save().then(function(value) {

					self.set('message','Please check the given e-mail for account activation details');
				}, function(reason) {
					// on rejection
					var emailIssues=reason.errors[0].email;
					if (emailIssues!==""){
						self.set('emailProblems',emailIssues);
					}

					var userIssues=reason.errors[0].username;
					if (userIssues!==""){
						self.set('usernameExists',userIssues);

					}
				});
			}	
		}
	}
});
