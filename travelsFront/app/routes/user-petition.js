import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import ENV from 'travels-front/config/environment'; 

const { get } = Ember;

export default Ember.Route.extend(AuthenticatedRouteMixin,{
	newPetition: true,
  modelName: 'user-petition',

	model(params) {
    let petitionId = params.petition_id;
    let model;
    if (petitionId && petitionId != "new") {
      // edit petition
      model = this.store.findRecord(this.modelName, petitionId);
      this.set('newPetition', false);
    } else {
      // create petition
      model = this.store.createRecord(this.modelName);
      this.set('newPetition', true);
      //set some default values to user petition
      this.store.findRecord('city', "5").then((athens) => {
        model.set('departure_point', athens);
      });
      model.set('means_of_transport', "AIR");
      model.set('meal', "NON");
    }
    
		return new Ember.RSVP.Promise(function(resolve, reject) {
      // resolve user profile
      this.store.findRecord('profile', 1).then(function(profile) {
        // if petition is new initialize it with user profile info
        if (this.get('newPetition')) {
          this.initializePetition(model, profile)
          resolve(model);
        } else {
          // delegate stuff to model promise
          return model.then(resolve).catch(reject);
        }
      }.bind(this));
    }.bind(this));
	},

  // copy common profile fields to petition object
	initializePetition(petition, profile) {

    let commonFields = [
      'first_name',
      'last_name',
      'iban',
      'specialty',
      'kind',
      'tax_reg_num',
      'tax_office',
      'category'
    ];

    for (let field of commonFields) {
      petition.set(field, get(profile, field));
    }
	},

  setupController(c) {
    this._super(...arguments);
    c.set('newPetition', get(this, 'newPetition'));
  },

	actions: {
	}
	
});
