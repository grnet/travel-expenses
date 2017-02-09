import {Petition} from 'travels-front/lib/models/petition';
import {validator, buildValidations} from 'ember-cp-validations';
import {UIS} from 'travels-front/lib/form-uis';
import {normalizePetition, serializePetition} from 'travels-front/lib/models/util';


var Validations = buildValidations({
  iban: [
    validator('presence', {presence: true}),
    validator('iban-validator')
  ],
  first_name: [
  	validator('presence', {presence: true}),
    validator('length', {min: 2})
  ],
  last_name: [
  	validator('presence', {presence: true}),
    validator('length', {min: 2})
  ],
  tax_reg_num: [
  	validator('presence', {presence: true}),
    validator('number', {allowString: true, integer: true}),
    validator('length', {is: 9}),
  ],
  specialty: validator('presence', {presence: true}),
  kind: validator('presence', {presence: true}),
  tax_office: validator('presence', {presence: true}),
});

export default Petition.extend(Validations, {
  __api__: {
    path: 'petition-user-saved/',
    normalize: normalizePetition, 
    serialize: serializePetition
  },
  __ui__: {
   'default': UIS['petition_user'],
  } 
});
