import {Petition, PetitionValidations} from 'travels-front/lib/models/petition';
import {UIS} from 'travels-front/lib/form-uis';

var Validations=PetitionValidations({
});

export default Petition(Validations, {
  __ui__: {
    "user": UIS['petition_user']
  }
});
