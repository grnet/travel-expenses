import Ember from 'ember';
import config from './config/environment';
import ENV from 'travels-front/config/environment'; 

const Router = Ember.Router.extend({
    location: config.locationType,
});

Router.map(function() {
  this.route('login');
  this.route('signup');
  this.route('profile');
  // this.route('petition', {path: 'petition/:petition_id'});
  // this.route('petitionList');
  // this.route('advancedPetition',{path:':ap_id'});
  // this.route('advancedList');
  this.route('userPetition', {path: 'userPetition/:petition_id'});
});

export default Router;
