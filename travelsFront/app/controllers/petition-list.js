import Ember from 'ember';
import ENV from 'travels-front/config/environment'; 

const {
  set,
  get
} = Ember;

export default Ember.Controller.extend({

  editPetitionRoute: 'userPetition',
  editCompensationRoute: 'userCompensation',
	deleteMessage: "",
	statePetitionList: "",
  sortByDse: ['status:desc', 'dse:asc'],
  sortedModel: Ember.computed.sort('model', 'sortByDse'),

	actions: {

		petitionUndo(petition) {
      petition.cancel().then(() => {
        set(this, 'actionMessage', 'petition.undo.success');
        get(this, 'model').reload();
      });
		},	

		petitionEdit(model){
      if (model.get('status') == 4) {
        this.transitionToRoute(get(this, 'editCompensationRoute'), model.get('id'));
      }
      else {
        this.transitionToRoute(get(this, 'editPetitionRoute'), model.get('id'));
      }
		},

		petitionDelete(model){
      if (model.get("currentState.stateName") == "root.deleted.inFlight") { return; }
      model.destroyRecord().then(() => {
        set(this, 'actionMessage', 'petition.delete.success');
      }, (err) => {
        console.error(err);
        set(this, 'actionMessage', 'petition.delete.fail')
      })
		}

	}
});
