import Ember from 'ember';

export function currentDate(/*params, hash*/) {
	return moment().format("YYYY-MM-DDTHH:mm:ssZ");
}

export default Ember.Helper.helper(currentDate);
