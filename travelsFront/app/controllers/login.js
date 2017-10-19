
import Ember from 'ember';


export default Ember.Controller.extend({

	session: Ember.inject.service('session'),

	actions: {
		authenticate: function() {
			var credentials = {
        'identification': this.get('model.username'),
        'password': this.get('model.login_pass')
      };

			var authenticator = 'authenticator:token';
			this.get('session').authenticate(authenticator, credentials).then(() => {
    			this.get("account").loadCurrentUser().then((profile) => {
            
            let group = profile.get('user_group');
            return profile.get('profileIsFilled').then((profileFilled) => {
              if (profileFilled) {
                if (group === "SECRETARY" || group === "CONTROLLER" || group === "VIEWER") {
                  this.transitionToRoute('advancedList');
                } else if (group === "USER") {
                  this.transitionToRoute('petitionList');
                } else if (group === "MANAGER") {
                  this.transitionToRoute('manager-list');
                } else if (group === "PRESIDENT_SECRETARY") {
                  this.transitionToRoute('president-list');
                }
              } 
              else {
                this.transitionToRoute('profile');
              }
            });
          });
			}).catch((err) => {
        if (err.non_field_errors) {
          this.set('submitError', err.non_field_errors[0]);
        } else {
          this.set('submitError', 'Login failed.')
        }
        let model = this.get("model");
      });
		}
	}
});

