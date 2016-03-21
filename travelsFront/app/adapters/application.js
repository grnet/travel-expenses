import DS from 'ember-data';

export default DS.RESTAdapter.extend({
	
	host: 'http://127.0.0.1:8000/api',
	contentType: 'application/json',
	dataType: 'json',
	
	headers: {
	 username: 'admin',
     password: 'admin'
    } 
   
});
