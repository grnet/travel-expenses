import Ember from 'ember';
import config from './config/environment';
import ENV from 'travels-front/config/environment'; 

const Router = Ember.Router.extend({
  location: config.locationType,
  rootURL: config.rootURL
});

Router.map(function() {
  this.route('login');
  this.route('signup');
  this.route('profile');
  this.route('petitionList');
  this.route('userPetition', {path: 'userPetition/:petition_id'});
  this.route('advancedList');
  this.route('subPetitionList');
  this.route('secretaryPetition');
});

export default Router;
