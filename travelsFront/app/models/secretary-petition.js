import {SecretaryPetition, SecretaryPetitionValidations} from 'travels-front/lib/models/secretary-petition';
import {UIS} from 'travels-front/lib/form-uis';

var Validations=SecretaryPetitionValidations({
});

export default Petition(Validations, {
  __ui__: {
    "user": UIS['petition_user'],
    "secretary": UIS['petition_travel']
  }
});
