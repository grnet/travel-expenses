import {Petition} from 'travels-front/lib/models/petition';
import {validator, buildValidations} from 'ember-cp-validations';
import {UIS} from 'travels-front/lib/form-uis';


var Validations = buildValidations({
  iban: validator('iban-validator'),
  email: [
    validator('presence', true),
    validator('format', { type: 'email' })
  ],

});


export default Petition.extend(Validations, {
  __api__: {
    path: 'petition/user/saved/',
  },
  __ui__: {
   'default': UIS['petition_user'],
  } 

});
