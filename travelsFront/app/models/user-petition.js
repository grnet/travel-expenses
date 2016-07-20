import {Petition} from 'travels-front/lib/models/petition';
import {UIS} from 'travels-front/lib/form-uis'; 

export default Petition.extend({
  __api__: {
    //ns: 'api',
    path: 'petition/user/saved/',
    buildURL: function(adapter, url, id, snap, rtype, query) {
      // always return my profile endpoint
      return this.urlJoin(adapter.get('host'), this.ns, this.path) + '/';
    }
  },
  __ui__: {
    'default': UIS['petition_user']
  }
});

