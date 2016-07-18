import {SecretaryPetition, SecretaryPetitionValidations} from 'travels-front/lib/models/secretary-petition';
import {UIS} from 'travels-front/lib/form-uis';

var Validations=SecretaryPetitionValidations({
  first_name: [
    validator('presence', true),
  ],
  taskstartdate: [
    validator('presence', true),
  ],

});

export default SecretaryPetition(Validations, {
  __ui__: {
    "user": UIS['petition_user'],
    "secretary": UIS['petition_travel']
  }
});
