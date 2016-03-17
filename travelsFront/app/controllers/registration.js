import Ember from 'ember';

export default Ember.Controller.extend({

	actions: {
		
		saveRegistration(){
			console.log('My name is: ', this.get('name'));
			

			this.store.createRecord('user',{
					type: 'user',
					name: this.get('name')
				
			});
			
		}
	}
});
