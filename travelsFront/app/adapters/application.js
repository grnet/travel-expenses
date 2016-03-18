import DS from 'ember-data';

export default DS.RESTAdapter.extend({
	host: 'http://127.0.0.1:8000/api',
	// type: 'GET',
	headers: {
	 username: 'admin',
     password: 'admin'
    } 
 //    contentType: 'application/json'
});
