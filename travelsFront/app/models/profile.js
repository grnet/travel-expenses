import Profile from 'ember-gen-apimas/models/profile';
import DS from 'ember-data';
import ENV from 'travel/config/environment';

const CHOICES = ENV.APP.resources;

export default  Profile.extend({
  __api__: {
    buildURL(adapter) {
      return adapter.host + '/auth/me/detailed';
    },
    normalize(user) {
      user.id = 'me';
      return user;
    }
  },

  username: DS.attr({formAttrs: {disabled: true}}),
  email: DS.attr('string'),
  first_name: DS.attr(),
  last_name: DS.attr(),
  iban: DS.attr(),
  specialty: DS.attr({type: 'select', choices: CHOICES.SPECIALTY}),
  kind: DS.attr({type: 'select', choices: CHOICES.KIND}),
  tax_reg_num: DS.attr(),
  tax_office: DS.belongsTo('tax-office', {formAttrs: {optionLabelAttr: 'full_label'}}),
  user_category: DS.attr({formAttrs: {disabled: true}, type: 'select', choices: CHOICES.USER_CATEGORY}),
  user_group: DS.attr(),
});
