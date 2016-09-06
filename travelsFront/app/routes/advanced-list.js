import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import {PetitionListRoute} from 'travels-front/lib/models/util';

export default PetitionListRoute.extend(AuthenticatedRouteMixin,{
  petitionModel: 'secretary-petition'
});
