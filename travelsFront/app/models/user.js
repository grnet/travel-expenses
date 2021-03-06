import DS from 'ember-data';
import ENV from 'travel/config/environment';

const CHOICES = ENV.APP.resources;

export default DS.Model.extend({
  username: DS.attr({ disabled: true }),
  email: DS.attr('string'),
  first_name: DS.attr({ disabled: true }),
  last_name: DS.attr({ disabled: true }),
  iban: DS.attr(),
  specialty: DS.attr({ type: 'select', choices: CHOICES.SPECIALTY }),
  kind: DS.attr({ type: 'select', choices: CHOICES.KIND }),
  tax_reg_num: DS.attr(),
  tax_office: DS.belongsTo('tax-office', { formAttrs: { optionLabelAttr: 'full_label' } }),
  user_category: DS.attr({ formAttrs: { disabled: true }, type: 'select', choices: CHOICES.USER_CATEGORY }),
  user_group: DS.attr(),
  is_active: DS.attr('boolean'),
  specialty_label: Ember.computed('specialty', function() {
    let specialty = this.get('specialty');

    for (let pair of CHOICES.SPECIALTY) {
      if (pair[0] === specialty) {
        return pair[1] || specialty;
      }
    }
  }),
  kind_label: Ember.computed('kind', function() {
    let kind = this.get('kind');

    for (let pair of CHOICES.KIND) {
      if (pair[0] === kind) {
        return pair[1] || kind;
      }
    }
  }),
  full_name: Ember.computed('first_name', 'last_name', function() {
    let firstName =  this.get('first_name');
    let lastName = this.get('last_name');

    return `${firstName} ${lastName}`;
  }),
});
