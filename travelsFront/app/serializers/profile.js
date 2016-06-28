import DS from 'ember-data';

export default DS.JSONSerializer.extend({
	primaryKey: 'username',

	normalizeErrorResponse: function(store, primaryModelClass, payload,id,requestType) {
		if (payload && typeof payload === 'object' && payload.errors) {
			return payload.errors;
		} else {
			return [
				{
					status: payload.status || status,
					title: payload.message,
					details: payload.details
				}
			];
		}
	}

});
