import {Petition, PetitionValidations} from 'travels-front/lib/models/petition';

var SecretaryPetitionValidations=PetitionValidations({
});

var SecretaryPetition = Petition({
  movement_protocol: DS.attr(),
});

export default {SecretaryPetition, SecretaryPetitionValidations};
