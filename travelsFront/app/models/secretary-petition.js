import {SecretaryPetition} from 'travels-front/lib/models/secretary-petition';
import {validator, buildValidations} from 'ember-cp-validations';
import {UIS} from 'travels-front/lib/form-uis';
import {normalizePetition, serializePetition} from 'travels-front/lib/models/util';


var Validations = buildValidations({
    iban: validator('iban-validator'),
});

export default SecretaryPetition.extend(Validations, {
  __api__: {
    path: 'petition-secretary-saved/',
    normalize: normalizePetition, 
    serialize: serializePetition
  },
  __ui__: {
   'default': UIS['petition_travel'],
  } 

});
