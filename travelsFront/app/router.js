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
});

export default Router;
