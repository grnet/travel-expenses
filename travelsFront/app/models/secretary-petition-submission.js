import {SecretaryPetition} from 'travels-front/lib/models/petition';
import {validator, buildValidations} from 'ember-cp-validations';
import {UIS} from 'travels-front/lib/form-uis';


var Validations=SecretaryPetitionValidations({
  first_name: [
    validator('presence', true),
  ],
  taskstartdate: [
    validator('presence', true),
  ],
});


export default SecretaryPetition.extend(Validations, {
  __api__: {
    path: 'petition/secretary/saved/',
  },
  __ui__: {
   'default': UIS['petition_user'],
  } 

});

