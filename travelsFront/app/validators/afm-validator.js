import BaseValidator from 'ember-cp-validations/validators/base';

export default BaseValidator.extend({
	validate(value/*, options, model, attribute*/) {
		if (value!=null && value!=''){	
			var intValue=Number(value);

			if (String(intValue)=='NaN') {
				return "AFM should not contain characters";
			}
			var length= value.length;

			if(length==null)
				length=9;

			if (length!=9) {
				return 'AFM should be 9 digits, current length:'+length;
			}
		}

		return true;
	}
});
