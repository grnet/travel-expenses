import {SecretaryPetition} from 'travels-front/lib/models/petition';
import {validator, buildValidations} from 'ember-cp-validations';
import {UIS} from 'travels-front/lib/form-uis';


var Validations = buildValidations({
    iban: validator('iban-validator'),
});


export default Petition.extend(Validations, {
  __api__: {
    path: 'petition/secretary/saved/',
  },
  __ui__: {
   'default': UIS['petition_user'],
  } 

});
