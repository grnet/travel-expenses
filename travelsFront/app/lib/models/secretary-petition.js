import {Petition} from 'travels-front/lib/models/petition';

export var SecretaryPetition = Petition.extend({
  movement_protocol: DS.attr(),
});
