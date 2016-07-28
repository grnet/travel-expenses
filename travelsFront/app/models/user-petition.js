import {Petition} from 'travels-front/lib/models/petition';
import {validator, buildValidations} from 'ember-cp-validations';
import {UIS} from 'travels-front/lib/form-uis';
import {normalizePetition, serializePetition} from 'travels-front/lib/models/util';


var Validations = buildValidations({
    iban: validator('iban-validator'),
});

export default Petition.extend(Validations, {
  __api__: {
    path: 'petition/user/saved/',
    normalize: normalizePetition, 
    serialize: serializePetition
  },
  __ui__: {
   'default': UIS['petition_user'],
  } 
});
