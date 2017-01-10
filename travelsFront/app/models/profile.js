import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travels-front/config/environment';

const { get } = Ember;

const CHOICES = ENV.APP.resource_choices;

export default DS.Model.extend({

  __api__: {
    namespace: 'auth',
    path: 'me/detailed',
    buildURL: function(adapter, url, id, snap, rtype, query) {
      // always return my profile endpoint
      let host = get(adapter, 'host'),
          namespace = get(this, 'namespace'),
          path = get(this, 'path');
      return this.urlJoin(host, namespace, path) + '/';
    }
  },

  
	username: DS.attr(),
	first_name: DS.attr(),
	last_name: DS.attr(),
  iban: DS.attr(),
  specialty: DS.attr({type: 'select', choices: CHOICES.SPECIALTY}),
  kind: DS.attr({type: 'select', choices: CHOICES.KIND}),
  tax_reg_num: DS.attr(),
  tax_office: DS.belongsTo('tax-office' ),
  user_category: DS.attr({formAttrs: { disabled: true}, type: 'select', choices: CHOICES.USER_CATEGORY}),
  user_group: DS.attr(),
});
