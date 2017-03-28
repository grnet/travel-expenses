import Profile from 'ember-gen-apimas/models/profile';
import DS from 'ember-data';
import ENV from 'travel/config/environment';

const CHOICES = ENV.APP.resources;

export default Profile.extend({
  username: DS.attr(),
  first_name: DS.attr(),
  last_name: DS.attr(),
  iban: DS.attr(),
  specialty: DS.attr({type: 'select', choices: CHOICES.SPECIALTY}),
  kind: DS.attr({type: 'select', choices: CHOICES.KIND}),
  tax_reg_num: DS.attr(),
  tax_office: DS.belongsTo('tax-office' ),
  user_category: DS.attr({formAttrs: {disabled: true}, type: 'select', choices: CHOICES.USER_CATEGORY}),
  user_group: DS.attr(),
});
