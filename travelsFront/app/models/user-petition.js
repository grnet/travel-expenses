import DS from 'ember-data';
import ENV from 'travel/config/environment';

const CHOICES = ENV.APP.resources;

export default DS.Model.extend({
	__api__: {
    path: '/petition-user-saved',
  },

	  // profile fields
  first_name: DS.attr(),
  last_name: DS.attr(),
  dse: DS.attr('string'),

});
