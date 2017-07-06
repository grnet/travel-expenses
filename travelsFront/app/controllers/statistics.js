import Ember from 'ember';
import ENV from 'travels-front/config/environment';

const {
  set,
  get,
  computed,
  on
} = Ember;

export default Ember.Controller.extend({

	session: Ember.inject.service('session'),

	actions: {

		statisticsExportPerProject(project_id, project_name) {

			var token = this.get("session.data.authenticated.auth_token");
			var filename = project_name + '_statistics_';
			var base_url = ENV.APP.backend_host;
   		var extension_url = "/project/"+project_id+"/project_stats/?response_format=csv";
      var date = moment().format('L');

    	return $.ajax({
	      headers:{
	        Authorization: 'Token ' + token
	      },
	      url: base_url + extension_url,

	      success: function(data) {
          var blob=new Blob([data], { type: "text/csv" });
          var link=document.createElement('a');
          link.href=window.URL.createObjectURL(blob);
          link.download=filename + date + '.csv';
          link.click();
      	}
    	});
		},

		statisticsExport() {

			var token = this.get("session.data.authenticated.auth_token");
			var filename = 'all_project_stats';
			var base_url = ENV.APP.backend_host;
   		var extension_url = "/project/stats/?response_format=csv";
      var date = moment().format('L');
    	
    	
    	return $.ajax({

	      headers:{
	        Authorization: 'Token ' + token
	      },
	      url: base_url + extension_url,

	      success: function(data) {

          var blob=new Blob([data], { type: "text/csv" });
          var link=document.createElement('a');
          link.href=window.URL.createObjectURL(blob);
          link.download=filename + date + '.csv';
          link.click();
      	}
    	});
		}
	}
});
