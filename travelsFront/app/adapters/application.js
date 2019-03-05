import BaseAdapter from 'ember-gen-apimas/adapters/application';
import { getCookie } from '../lib/common';

var csrftoken = getCookie('csrftoken');
export default BaseAdapter.extend({

  headers: function() {
    return {
      'X-CSRFToken': csrftoken,
    };
  }.property().volatile()
});
