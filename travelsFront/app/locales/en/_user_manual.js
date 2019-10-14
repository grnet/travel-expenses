import ENV from 'travel/config/environment';

const travel_report_template = ENV.APP.links.travel_report_template;
const manual = {
  'user.application.new': 
    '<h4>' + 'Create new Travel Application' + '</h4>' + 
    '<p>' + 
      'The traveler should visit the tab "Applications" and select the "Create" button, in order to create a new travel application. The traveler should then provide the following information: (required fields are marked with a *)' + 
      '<ul>' + 
        '<li>' + 'Project (Drop-down list) *' + '</li>' + 
        '<li>' + 'Travel reason *' + '</li>' + 
        '<li>' + 'Task start date * (at the local time of the destination)' + '</li>' + 
        '<li>' + 'Task end date * (at the local time of the destination)' + '</li>' + 
        '<li>' + 'Departure - From *' + '</li>' + 
        '<li>' + 'Destination - To *' + '</li>' + 
        '<li>' + 'Departure datetime (at the local time of the departure city)' + '</li>' + 
        '<li>' + 'Return datetime (at the local time of the destination city)' + '</li>' + 
        '<li>' + 'Participation Cost - Local Currency: attendance at conferences, workshops, etc (in the local currency of the country of destination)' + '</li>' + 
        '<li>' + 'Traveler recommendations (for flight/hotel reservations, etc)' + '</li>' + 
      '</ul>' + 
      'The traveler should first save his/her changes and then submit the application. Note that there is no limit to how many times the application can be saved until it is submitted. Upon application submission the  Project Manager and the Secretary will be notified by email.' + 
      '<br>' + '<br>' + 
    '</p>', 
  'user.applications': 
      '<p>' + 
        'From the "Applications" tab, the traveler can perform the following actions:' + 
      '<ul>' + 
        '<li>' + '<b>' + 'View details' + '</b>' + '</li>' + 
        '<li>' + '<b>' + 'Edit or Submit' + '</b>' + ': if the application is in status "Processed by traveler"' + '</li>' + 
        '<li>' + '<b>' + 'Delete' + '</b>' + ': if the application is in status "Processed by traveler"' + '</li>' + 
        '<li>' + '<b>' + 'Undo submission' + '</b>' + ': if the application has been submitted and the Secretary has not processed it yet' + '</li>' + 
      '</ul>' +   
      '</p>', 
  'user.compensation':
    '<h4>' + 'Create Application for Compensation' + '</h4>' + 
    '<p>' + 'After the traveler\'s return, he/she should log into the system and complete the following details:' + 
    '<ul>' + 
      '<li>' + '<b>' + 'File upload' + '</b>' + ': The traveler should upload a .zip file with at least: (1) the agenda and (2) the travel report according to ( ' + '<a href='+travel_report_template+'>' + 'template' + '</a>' + ' ). The .zip file should not exceed 8 MB.' + '</li>' +
      '<li>' + '<b>' + 'Additional Expenses' + '</b>' + ': The traveler should enter the total travel costs, by adding all public transport tickets (actual price).' + '</li>' + 
      '<li>' + '<b>' + 'Additional Expenses - Description' + '</b>' + ': description of costs e.g. bus tickets.' + '</li>' + 
    '</ul>' + 
    'The traveler should first save his/her changes and then submit the application. Note that there is no limit to how many times the application can be saved until it is submitted.' + 
    '<br>' + '<br>' + 
    '</p>',
  'user.actions':
      '<h4>' + 'Traveler Actions' + '</h4>' + 
      '<p>' + 'Below we will present all the statuses of an application. The following table lists the application statuses as well as the actions that the traveler can perform depending on the application status:' + 
      '<div class="container">' + 
      '<table class="manualTable">' + 
        '<thead>' + 
          '<tr>' + 
            '<th>' + 'Status' + '</th>' + 
            '<th>' + 'Description' + '</th>' + 
            '<th>' + 'Actions' + '</th>' + 
          '</tr>' + 
        '</thead>' + 
        '<tbody>' + 
          '<tr>' + 
            '<td>' + '1' + '</td>' + 
            '<td>' + 'Processed by Traveler' + '</td>' + 
            '<td>' + 'Edit, Save and Submit, Delete' + '</td>' + 
          '</tr>' + 
          '<tr>' + 
            '<td>' + '2' + '</td>' + 
            '<td>' + 'Submitted by Traveler' + '</td>' + 
            '<td>' + 'Undo submission' + '</td>' + 
          '</tr>' + 
          '<tr>' + 
            '<td>' + '3' + '</td>' + 
            '<td>' + 'Processed by Secretary' + '</td>' + 
            '<td>' + '-' + '</td>' + 
          '</tr>' + 
          '<tr>' + 
            '<td>' + '4' + '</td>' + 
            '<td>' + 'Finalized by Secretary' + '</td>' + 
            '<td>' + '-' + '</td>' + 
          '</tr>' + 
          '<tr>' + 
            '<td>' + '5' + '</td>' + 
            '<td>' + 'Movement Desicion signed by President' + '</td>' + 
            '<td>' + 'Edit, Save and Submit, Export' + '</td>' + 
          '</tr>' + 
          '<tr>' + 
            '<td>' + '6' + '</td>' + 
            '<td>' + 'Processed by Traveler for Compensation' + '</td>' + 
            '<td>' + 'Edit, Save and Submit, Export' + '</td>' + 
          '</tr>' + 
          '<tr>' + 
            '<td>' + '7' + '</td>' + 
            '<td>' + 'Submitted by Traveler for Compensation/td>' + 
            '<td>' + 'Undo submission' + '</td>' + 
          '</tr>' + 
          '<tr>' + 
            '<td>' + '8' + '</td>' + 
            '<td>' + 'Processed - Auditing' + '</td>' + 
            '<td>' + '-' + '</td>' + 
          '</tr>' + 
          '<tr>' + 
            '<td>' + '9' + '</td>' + 
            '<td>' + 'Finalized - Auditing' + '</td>' + 
            '<td>' + '-' + '</td>' + 
          '</tr>' + 
          '<tr>' + 
            '<td>' + '10' + '</td>' + 
            '<td>' + 'Compensation Desicion signed by President' + '</td>' + 
            '<td>' + '-' + '</td>' + 
          '</tr>' + 
        '</tbody>' + 
      '</table>' + 
      '</div>',
};

export { manual };
