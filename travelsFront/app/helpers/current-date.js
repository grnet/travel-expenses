import Ember from 'ember';

export function currentDate(/*params, hash*/) {
	return moment().format("YYYY-MM-DDTHH:mm:ssZ");
	//return moment().format("YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]");
}

export default Ember.Helper.helper(currentDate);
