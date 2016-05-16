import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
    location: config.locationType
});

Router.map(function() {
  this.route('login');
  this.route('signup');
  this.route('profile');
  this.route('specialty');
  this.route('kind');
  this.route('petition');
  this.route('petitionList');
  this.route('editPetition', {path: ':petition_id'});
  
});

export default Router;
