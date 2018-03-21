import Ember from 'ember';
import {field} from 'ember-gen';
import validate from 'ember-gen/validate';

const FS_VALIDATORS = {
  first_name: [validate.presence(true)],
  last_name: [validate.presence(true)],
  specialty: [validate.presence(true)],
  kind: [validate.presence(true)],
  tax_reg_num: [validate.presence(true)],
  tax_office: [validate.presence(true)],
  iban: [validate.presence(true)],
};

const FS_DETAILS = {
  label: 'user_data.label',
  fields: [
   field('first_name', { disabled: true }),
   field('last_name', { disabled: true }),
   field('specialty_label', { disabled: true }),
   field('kind_label', { disabled: true }),
   field('tax_reg_num', { disabled: true }),
   field('tax_office.name', { disabled: true }),
   field('iban', { disabled: true }),
   field('user_category', { disabled: true }),
  ],
  layout: {
    flex: [50, 50, 50, 50, 50, 50, 50, 50]
  }
};

const FS_EDIT = [
  {
    label: 'my_account.label',
    fields: ['username', 'email'],
    layout: {
      flex: [50, 50]
    }
  },
  {
    label: 'user_data.label',
    fields: [
      'first_name',
      'last_name',
      'specialty',
      'kind',
      'tax_reg_num',
      'tax_office',
      'iban',
      'user_category',
    ],
    layout: {
      flex: [50, 50, 50, 50, 50, 50, 50, 50]
    }
  }
];

export { FS_DETAILS, FS_EDIT, FS_VALIDATORS };