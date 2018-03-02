import Ember from 'ember';
import {field} from 'ember-gen';

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

export { FS_DETAILS };