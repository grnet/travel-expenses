import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

export default Ember.Controller.extend({

	actions: {
		petitionUndo(petition) {
      petition.cancel().then(() => {
        this.transitionToRoute('petitionList').then(function(r) {
          petition.unloadRecord();
        });
      });
		},	
	}
});
