import Ember from 'ember';
import config from './config/environment';
import ENV from 'travels-front/config/environment'; 

const Router = Ember.Router.extend({
  location: config.locationType,
  rootURL: config.rootURL
});

Router.map(function() {
  this.route('signup');
  this.route('login');
  this.route('profile');
  this.route('petitionList');
  this.route('subPetitionList');
  this.route('userPetition', {path: 'userPetition/:petition_id'});
  this.route('advancedList');
  this.route('secretaryPetition', {path: 'secretaryPetition/:petition_id'});
  this.route('userCompensation', {path: 'userCompensation/:petition_id'});
  this.route('secretaryCompensation', {path: 'secretaryCompensation/:petition_id'});
  this.route('password');
  this.route('help');
});

export default Router;
