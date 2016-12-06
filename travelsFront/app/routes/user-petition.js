import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import ENV from 'travels-front/config/environment'; 

const { get } = Ember;

export default Ember.Route.extend(AuthenticatedRouteMixin,{

  beforeModel: function() {

    this.store.findRecord('profile', 1).then((profile) => {
      return profile.get('profileIsFilled').then((profileFilled) => {
        if (profileFilled) {
          this.transitionTo('userPetition');             
        } 
        else {
          this.transitionTo('profile');
        }              
      });
    });
  },

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
    }
    
		return new Ember.RSVP.Promise(function(resolve, reject) {
      // resolve user profile
      this.store.findRecord('profile', 1).then(function(profile) {
        // if petition is new initialize it with user profile info
        if (this.get('newPetition')) {
          this.initializePetition(model, profile).then(resolve);
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
      'user_category'
    ];

    for (let field of commonFields) {
      petition.set(field, get(profile, field));
    }

    let self = this;
    return new Ember.RSVP.Promise(function(resolve, reject) {
      petition.set('means_of_transport', "AIR");
      petition.set('meals', "NON");
      petition.set('participation_local_currency', "EUR");
      petition.set('accommodation_local_currency', "EUR");
      //set some default values to user petition
      self.store.findRecord('city', ENV.default_city).then((defaultCity) => {
        petition.set('departure_point', defaultCity);
        profile.get('tax_office').then((office) => {
          petition.set('tax_office',office);
          resolve(petition);
        });
      }).catch(function() {
        resolve(petition);
      });
    })
	},

  setupController(c) {
    this._super(...arguments);
    c.set('newPetition', get(this, 'newPetition'));
  },

	actions: {
	}
	
});
