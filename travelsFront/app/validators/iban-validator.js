import Ember from 'ember';
import BaseValidator from 'ember-cp-validations/validators/base';

export default BaseValidator.extend({
	validate(value/*, options, model, attribute*/) {


		if (value!=null &&  value!='') {
			value=value.trim();


			var	valueLength=value.length;
			if (valueLength>=1 && valueLength!=27) {
				return "IBAN should be a 27 letters alphanumeric,current length:"+valueLength;
			}
			var value_upper=value.toUpperCase();
			var	countryCode=value.substring(0,2);

			if (value!==value_upper) {
				return "IBAN country code:" + countryCode + " should be in Uppercase mode";

			}

			if (countryCode!=='GR') {
				return "IBAN country code:" + countryCode + " is not GR";
			}

			var	iban_check_digits =value.substring(2,4); 
			var iban_check_digits_num=Number(iban_check_digits);

			if (String(iban_check_digits_num)=='NaN') {
				return "IBAN should contain only numbers apart from the first 2 letters (GR),IBAN check digits are problematic";
			}

			var bban=value.substring(4,value.length);

			var bank_code=bban.substring(0,3);
			var bank_code_num=Number(bank_code);
			if (String(bank_code_num)=='NaN') {
				return "IBAN should contain only numbers apart from the first 2 letters (GR),Bank Code value is problematic";
			}

			var bank_store=bban.substring(3,7);
			var bank_store_num=Number(bank_store);
			if (String(bank_store_num)=='NaN') {
				return "IBAN should contain only numbers apart from the first 2 letters (GR),Bank Store value is problematic";
			}

			var customer_code=bban.substring(7,bban.length);
			var customer_code_num=Number(customer_code);
			if (String(customer_code_num)=='NaN') {
				return "IBAN should contain only numbers apart from the first 2 letters (GR),Customer Code value is problematic";
			}
		}
		return true;

	}
});
