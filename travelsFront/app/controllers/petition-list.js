import Ember from 'ember';
import ENV from 'travels-front/config/environment';
import {PetitionListRoute, preloadPetitions} from 'travels-front/lib/models/util';
import PaginationMixin from 'travels-front/mixins/pagination';

const {
  set,
  get,
  computed,
  on
} = Ember;

export default Ember.Controller.extend(PaginationMixin, {

  initFilters: on('init', function() {
    set(this, 'filters', {});
    set(this, 'activeFilters', {});
  }),

  editPetitionRoute: 'userPetition',
  editCompensationRoute: 'userCompensation',
  deleteMessage: "",
  statePetitionList: "",
  sortByDse: ['status:desc', 'dse:asc'],
  sortedModel: Ember.computed.sort('model', 'sortByDse'),

  filteredModel: computed('activeFilters', 'model.[]', function() {
    let filters = this.get('activeFilters'); 
    if (!filters) { return this.get('model'); } 

    if (filters.project) { filters.project = get(filters, 'project.id'); }
    if (filters.status) { filters.status = get(filters, 'status').substring(0, this.get('filters.status').indexOf(":")); }
    if (filters.depart_date__gte) { filters.depart_date__gte = moment(get(filters, 'depart_date__gte')).format("YYYY-MM-DD"); }
    if (filters.depart_date__lte) { filters.depart_date__lte = moment(get(filters, 'depart_date__lte')).format("YYYY-MM-DD"); }
    if (filters.return_date__lte) { filters.return_date__lte = moment(get(filters, 'return_date__lte')).format("YYYY-MM-DD"); }
    let promise = preloadPetitions(get(this, 'petitionModel'), this.store, filters);
    return DS.PromiseArray.create({promise});
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

    petitionWithdraw(petition){
      petition.withdraw().then(() => {
        get(this, 'model').reload();
      });
    },

    petitionWithdrawCancel(petition){
      petition.withdrawCancel().then(() => {
        get(this, 'model').reload();
      });
    },

    managerApproval(petition){
      petition.set('manager_movement_approval', "approved");
      Ember.RSVP.all([
        petition.get('tax_office'),
        petition.get('project'),
        petition.get('arrival_point'),
        petition.get('departure_point')
      ]).then(() => {
        petition.save();
      });
    },

    managerCostApproval(petition){
      petition.set('manager_cost_approval', "approved");
      Ember.RSVP.all([
        petition.get('tax_office'),
        petition.get('project'),
        petition.get('arrival_point'),
        petition.get('departure_point')
      ]).then(() => {
        petition.save();
      });
    }, 

    petitionDelete(model){
      if (model.get("currentState.stateName") == "root.deleted.inFlight") { return; }
      model.destroyRecord().then(() => {
        get(this, 'model').reload();
      }, (err) => {
        console.error(err);
        set(this, 'actionMessage', 'petition.delete.fail')
      })
    },

    setFilters(filters) {
      set(this, 'activeFilters', filters);
    }

  }
});
