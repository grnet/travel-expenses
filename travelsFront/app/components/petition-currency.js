import Ember from 'ember';
import Select from './model-form/fields/select';
import _ from 'lodash/lodash';
import ENV from 'travels-front/config/environment'; 

const {
  get,
  set,
  isArray,
  computed,
  computed: { alias, equal },
  observer
} = Ember;

export default Select.extend({
  layoutName: 'components/model-form/fields/select',

  observechoice: observer('object.arrival_point', function() {
    var local = this.get('object.arrival_point.country.currency');
    if (!(_.isUndefined(local)) && (local!= ENV.default_currency)  ) {
      this.get('field').set('choices', [[ENV.default_currency, ENV.default_currency], [local, local]]);
    } else {
      this.get('field').set('choices', [[ENV.default_currency, ENV.default_currency]]);
    }
  })
});
