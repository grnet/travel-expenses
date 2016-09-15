import {Compensation} from 'travels-front/lib/models/compensation';
import {validator, buildValidations} from 'ember-cp-validations';
import {UIS} from 'travels-front/lib/form-uis';
import {normalizePetition, serializePetition} from 'travels-front/lib/models/util';


var Validations = buildValidations({
    iban: validator('iban-validator'),
});

export default Compensation.extend(Validations, {
  __api__: {
    path: 'petition/user/compensations/',
    normalize: normalizePetition, 
    serialize: serializePetition
  },
  __ui__: {
   'default': UIS['compensation_user'],
  } 
});