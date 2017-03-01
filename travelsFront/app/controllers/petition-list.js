import Ember from 'ember';
import ENV from 'travels-front/config/environment';
import {PetitionListRoute, preloadPetitions} from 'travels-front/lib/models/util';
import PaginationMixin from 'travels-front/mixins/pagination';

const {
  set,
  get,
  computed
} = Ember;

export default Ember.Controller.extend(PaginationMixin, {

  editPetitionRoute: 'userPetition',
  editCompensationRoute: 'userCompensation',
	deleteMessage: "",
	statePetitionList: "",
  sortByDse: ['status:desc', 'dse:asc'],
  sortedModel: Ember.computed.sort('model', 'sortByDse'),
  filters: null,
  filteredModel: computed('filters', 'model.length', function() {
    let filters = this.get('filters');   console.log('filters in cotnroller', filters); 
    if (!filters) { return this.get('model'); } 
    
    return this.store.query('secretary-compensation', filters);
  }),

	actions: {

		petitionUndo(petition) {
      petition.cancel().then(() => {
        set(this, 'actionMessage', 'petition.undo.success');
        get(this, 'model').reload();
      });
		},

    pdfExport(petition, pdf_id) {
      petition.pdfExport(petition, pdf_id).then(() => {
        get(this, 'model').reload();
      });
    },

		petitionEdit(model){
      if (model.get('status') >= 4) {
        this.transitionToRoute(get(this, 'editCompensationRoute'), model.get('id'));
      }
      else {
        this.transitionToRoute(get(this, 'editPetitionRoute'), model.get('id'));
      }
		},

    //TO DO: Fix this to redirect to a view mode route
    petitionView(model){
      this.transitionToRoute(get(this, 'editCompensationRoute'), model.get('id'));
    },

    presidentApproval(petition){
      petition.approve().then(() => {
        get(this, 'model').reload();
      });
    },

		petitionDelete(model){
      if (model.get("currentState.stateName") == "root.deleted.inFlight") { return; }
      model.destroyRecord().then(() => {
        set(this, 'actionMessage', 'petition.delete.success');
      }, (err) => {
        console.error(err);
        set(this, 'actionMessage', 'petition.delete.fail')
      })
    },

    setFilters(filters) {
      set(this, 'filters', filters);
    }

	}
});
