import {SecretaryCompensation} from 'travels-front/lib/models/secretary-compensation';
import {validator, buildValidations} from 'ember-cp-validations';
import {UIS} from 'travels-front/lib/form-uis';
import {normalizePetition, serializePetition} from 'travels-front/lib/models/util';


export default SecretaryCompensation.extend(Validations, {
  __api__: {
    path: '',
    normalize: normalizePetition, 
    serialize: serializePetition
  },
  __ui__: {
   'default': UIS['compensation_secretary'],
  } 
});
