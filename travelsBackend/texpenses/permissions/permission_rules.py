PERMISSION_RULES = [
    ('tax-office', 'list', 'ADMIN', '*', '*', '*'),
    ('tax-office', 'list', 'anonymous', '*', '*', '*'),
    ('tax-office', 'list', 'USER', '*', '*', '*'),
    ('tax-office', 'list', 'SECRETARY', '*', '*', '*'),
    ('tax-office', 'list', 'CONTROLLER', '*', '*', '*'),
    ('tax-office', 'list', 'MANAGER', '*', '*', '*'),
    ('tax-office', 'list', 'VIEWER', '*', '*', '*'),
    ('tax-office', 'list', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('tax-office', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('tax-office', 'retrieve', 'anonymous', '*', '*', '*'),
    ('tax-office', 'retrieve', 'USER', '*', '*', '*'),
    ('tax-office', 'retrieve', 'SECRETARY', '*', '*', '*'),
    ('tax-office', 'retrieve', 'CONTROLLER', '*', '*', '*'),
    ('tax-office', 'retrieve', 'MANAGER', '*', '*', '*'),
    ('tax-office', 'retrieve', 'VIEWER', '*', '*', '*'),
    ('tax-office', 'retrieve', 'PRESIDENT_SECRETARY', '*', '*', '*'),


    ('project', 'list', 'ADMIN', '*', '*', '*'),
    ('project', 'list', 'anonymous', '*', '*', '*'),
    ('project', 'list', 'USER', '*', '*', '*'),
    ('project', 'list', 'SECRETARY', '*', '*', '*'),
    ('project', 'list', 'CONTROLLER', '*', '*', '*'),
    ('project', 'list', 'MANAGER', '*', '*', '*'),
    ('project', 'list', 'VIEWER', '*', '*', '*'),
    ('project', 'list', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('project', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('project', 'retrieve', 'anonymous', '*', '*', '*'),
    ('project', 'retrieve', 'USER', '*', '*', '*'),
    ('project', 'retrieve', 'SECRETARY', '*', '*', '*'),
    ('project', 'retrieve', 'CONTROLLER', '*', '*', '*'),
    ('project', 'retrieve', 'MANAGER', '*', '*', '*'),
    ('project', 'retrieve', 'VIEWER', '*', '*', '*'),
    ('project', 'retrieve', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('project', 'project_stats', 'CONTROLLER', '*', '*', '*'),
    ('project', 'project_stats', 'ADMIN', '*', '*', '*'),
    ('project', 'stats', 'ADMIN', '*', '*', '*'),
    ('project', 'stats', 'CONTROLLER', '*', '*', '*'),

    ('countries', 'list', 'ADMIN', '*', '*', '*'),
    ('countries', 'list', 'anonymous', '*', '*', '*'),
    ('countries', 'list', 'USER', '*', '*', '*'),
    ('countries', 'list', 'SECRETARY', '*', '*', '*'),
    ('countries', 'list', 'CONTROLLER', '*', '*', '*'),
    ('countries', 'list', 'MANAGER', '*', '*', '*'),
    ('countries', 'list', 'VIEWER', '*', '*', '*'),
    ('countries', 'list', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('countries', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('countries', 'retrieve', 'anonymous', '*', '*', '*'),
    ('countries', 'retrieve', 'USER', '*', '*', '*'),
    ('countries', 'retrieve', 'SECRETARY', '*', '*', '*'),
    ('countries', 'retrieve', 'CONTROLLER', '*', '*', '*'),
    ('countries', 'retrieve', 'MANAGER', '*', '*', '*'),
    ('countries', 'retrieve', 'VIEWER', '*', '*', '*'),
    ('countries', 'retrieve', 'PRESIDENT_SECRETARY', '*', '*', '*'),

    ('city', 'list', 'ADMIN', '*', '*', '*'),
    ('city', 'list', 'anonymous', '*', '*', '*'),
    ('city', 'list', 'USER', '*', '*', '*'),
    ('city', 'list', 'SECRETARY', '*', '*', '*'),
    ('city', 'list', 'CONTROLLER', '*', '*', '*'),
    ('city', 'list', 'MANAGER', '*', '*', '*'),
    ('city', 'list', 'VIEWER', '*', '*', '*'),
    ('city', 'list', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('city', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('city', 'retrieve', 'anonymous', '*', '*', '*'),
    ('city', 'retrieve', 'USER', '*', '*', '*'),
    ('city', 'retrieve', 'SECRETARY', '*', '*', '*'),
    ('city', 'retrieve', 'CONTROLLER', '*', '*', '*'),
    ('city', 'retrieve', 'MANAGER', '*', '*', '*'),
    ('city', 'retrieve', 'VIEWER', '*', '*', '*'),
    ('city', 'retrieve', 'PRESIDENT_SECRETARY', '*', '*', '*'),

    ('users', 'retrieve', 'USER', '*', 'isme', '*'),
    ('users', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('users', 'retrieve', 'SECRETARY', '*', 'isme', '*'),
    ('users', 'retrieve', 'CONTROLLER', '*', 'isme', '*'),
    ('users', 'retrieve', 'MANAGER', '*', 'isme', '*'),
    ('users', 'retrieve', 'VIEWER', '*', 'isme', '*'),
    ('users', 'retrieve', 'PRESIDENT_SECRETARY', '*', 'isme', '*'),

#==============================================================================

    # user
    ('applications', 'create', 'USER', '*', '*', '*'),
    ('applications', 'list', 'USER', '*', '*', '*'),
    ('applications', 'retrieve', 'USER', '*', '*', '*'),
    ('applications', 'destroy', 'USER', '*', 'usersaved', '*'),
    ('applications', 'submit', 'USER', '*', 'usersaved', '*'),
    ('applications', 'submit', 'USER', '*', 'usercompensationsaved', '*'),

    ('applications', 'cancel', 'USER', '*', 'usersubmitted', '*'),
    ('applications', 'cancel', 'USER', '*', 'usercompensationsubmitted', '*'),

    ('applications', 'application_report', 'USER', '*', 'usercompensationsaved', '*'),
    ('applications', 'application_report', 'USER', '*', 'presidentapproved', '*'),

    ('applications', 'update', 'USER', 'project', 'usersaved', '*'),
    ('applications', 'update', 'USER', 'reason', 'usersaved', '*'),
    ('applications', 'update', 'USER', 'task_start_date', 'usersaved', '*'),
    ('applications', 'update', 'USER', 'task_end_date', 'usersaved', '*'),
    ('applications', 'update', 'USER', 'participation_cost', 'usersaved', '*'),
    ('applications', 'update', 'USER', 'user_recommendation', 'usersaved', '*'),
    ('applications', 'update', 'USER', 'travel_info/departure_point','usersaved', '*'),
    ('applications', 'update', 'USER', 'travel_info/arrival_point','usersaved', '*'),
    ('applications', 'update', 'USER', 'travel_info/depart_date','usersaved', '*'),
    ('applications', 'update', 'USER', 'travel_info/return_date','usersaved', '*'),

    ('applications', 'update', 'USER', 'travel_info/departure_point','usercompensationsaved', '*'),
    ('applications', 'update', 'USER', 'travel_info/arrival_point','usercompensationsaved', '*'),
    ('applications', 'update', 'USER', 'travel_info/depart_date','usercompensationsaved', '*'),
    ('applications', 'update', 'USER', 'travel_info/return_date','usercompensationsaved', '*'),
    ('applications', 'update', 'USER', 'travel_files','usercompensationsaved', '*'),
    ('applications', 'update', 'USER', 'travel_report','usercompensationsaved', '*'),
    ('applications', 'update', 'USER', 'additional_expenses','usercompensationsaved', '*'),
    ('applications', 'update', 'USER', 'additional_expenses_default_currency','usercompensationsaved', '*'),
    ('applications', 'update', 'USER', 'additional_expenses_description','usercompensationsaved', '*'),

    ('applications', 'update', 'USER', 'travel_info/departure_point','presidentapproved', '*'),
    ('applications', 'update', 'USER', 'travel_info/arrival_point','presidentapproved', '*'),
    ('applications', 'update', 'USER', 'travel_info/depart_date','presidentapproved', '*'),
    ('applications', 'update', 'USER', 'travel_info/return_date','presidentapproved', '*'),
    ('applications', 'update', 'USER', 'travel_files','presidentapproved', '*'),
    ('applications', 'update', 'USER', 'travel_report','presidentapproved', '*'),
    ('applications', 'update', 'USER', 'additional_expenses','presidentapproved', '*'),
    ('applications', 'update', 'USER', 'additional_expenses_default_currency','presidentapproved', '*'),
    ('applications', 'update', 'USER', 'additional_expenses_description','presidentapproved', '*'),

    # viewer
    ('applications', 'list', 'VIEWER', '*','*', '*'),
    ('applications', 'retrieve', 'VIEWER', '*','*','*'),

    #manager
    ('applications', 'create', 'MANAGER', '*', '*', '*'),
    ('applications', 'list', 'MANAGER', '*', '*', '*'),
    ('applications', 'application_report', 'MANAGER', '*', 'usercompensationsaved', '*'),
    ('applications', 'application_report', 'MANAGER', '*', 'presidentapproved', '*'),

    ('applications', 'retrieve', 'MANAGER', '*', '*', '*'),
    ('applications', 'destroy', 'MANAGER', '*', 'usersaved', '*'),
    ('applications', 'submit', 'MANAGER', '*', 'usersaved', '*'),
    ('applications', 'submit', 'MANAGER', '*', 'usercompensationsaved', '*'),
    ('applications', 'cancel', 'MANAGER', '*',  'usersaved', '*'),
    ('applications', 'cancel', 'MANAGER', '*', 'usercompensationsubmitted', '*'),

    ('applications', 'update', 'MANAGER', 'manager_movement_approval', 'usersubmitted', '*'),
    ('applications', 'update', 'MANAGER', 'project', 'usersaved', '*'),
    ('applications', 'update', 'MANAGER', 'reason', 'usersaved', '*'),
    ('applications', 'update', 'MANAGER', 'task_start_date', 'usersaved', '*'),
    ('applications', 'update', 'MANAGER', 'task_end_date', 'usersaved', '*'),
    ('applications', 'update', 'MANAGER', 'participation_cost', 'usersaved', '*'),
    ('applications', 'update', 'MANAGER', 'user_recommendation', 'usersaved','*'),
    ('applications', 'update', 'MANAGER', 'travel_info/departure_point','usersaved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/arrival_point','usersaved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/depart_date','usersaved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/return_date','usersaved', '*'),

    ('applications', 'update', 'MANAGER', 'travel_info/departure_point','usercompensationsaved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/arrival_point','usercompensationsaved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/depart_date','usercompensationsaved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/return_date','usercompensationsaved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_files','usercompensationsaved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_report','usercompensationsaved', '*'),
    ('applications', 'update', 'MANAGER', 'additional_expenses','usercompensationsaved', '*'),
    ('applications', 'update', 'MANAGER', 'additional_expenses_default_currency','usercompensationsaved', '*'),
    ('applications', 'update', 'MANAGER', 'additional_expenses_description','usercompensationsaved', '*'),

    ('applications', 'update', 'MANAGER', 'travel_info/departure_point','presidentapproved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/arrival_point','presidentapproved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/depart_date','presidentapproved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/return_date','presidentapproved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_files','presidentapproved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_report','presidentapproved', '*'),
    ('applications', 'update', 'MANAGER', 'additional_expenses','presidentapproved', '*'),
    ('applications', 'update', 'MANAGER', 'additional_expenses_default_currency','presidentapproved', '*'),
    ('applications', 'update', 'MANAGER', 'additional_expenses_description','presidentapproved', '*'),

     #secretary
    ('applications', 'list', 'SECRETARY', '*','*','*'),
    ('applications', 'retrieve', 'SECRETARY', '*','*','*'),
    ('applications', 'update', 'SECRETARY', 'project', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'dse', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'reason', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'task_start_date', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'task_end_date', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'participation_cost', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'participation_payment_way', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'participation_payment_description', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'additional_expenses_initial', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'additional_expenses_initial_description', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'additional_expenses_default_currency', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'non_grnet_quota', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'secretary_recommendation', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/departure_point','secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/arrival_point','secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/depart_date','secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/return_date','secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/means_of_transport', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/transportation_cost', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/transportation_payment_description', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/meals', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_cost', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_default_currency', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_local_cost', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_payment_way', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_payment_description', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/transport_days_manual', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/overnights_num_manual', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/compensation_days_manual', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'movement_id', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'movement_date_protocol', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'movement_protocol', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'expenditure_protocol', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'expenditure_date_protocol', 'secretarysaved', '*'),


    ('applications', 'update', 'SECRETARY', 'project', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'dse', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'reason', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'task_start_date', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'task_end_date', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'participation_cost', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'participation_payment_way', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'participation_payment_description', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'additional_expenses_initial', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'additional_expenses_initial_description', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'additional_expenses_default_currency', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'non_grnet_quota', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'secretary_recommendation', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/departure_point','usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/arrival_point','usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/depart_date','usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/return_date','usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/means_of_transport', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/transportation_cost', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/transportation_payment_description', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/meals', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_cost', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_default_currency', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_local_cost', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_payment_way', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_payment_description', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/transport_days_manual', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/overnights_num_manual', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/compensation_days_manual', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'movement_id', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'movement_date_protocol', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'movement_protocol', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'expenditure_protocol', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'expenditure_date_protocol', 'usersubmitted', '*'),

    ('applications', 'submit', 'SECRETARY', '*', 'secretarysaved', '*'),
    ('applications', 'president_approval', 'SECRETARY', '*', 'secretarysubmitted', '*'),
    ('applications', 'application_report', 'SECRETARY', '*', 'secretarysubmitted', '*'),
    ('applications', 'decision_report', 'SECRETARY', '*', 'secretarysubmitted', '*'),
    ('applications', 'cancel', 'SECRETARY', '*', 'secretarysubmitted', '*'),


    #controller
    ('applications', 'list', 'CONTROLLER', '*','*','*'),
    ('applications', 'retrieve', 'CONTROLLER', '*','*','*'),
    ('applications', 'update', 'CONTROLLER', 'timesheeted', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'additional_expenses', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'additional_expenses_default_currency', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'additional_expenses_description', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'participation_cost', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'participation_local_cost', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'participation_default_currency', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'participation_payment_description', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'non_grnet_quota', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/transportation_cost', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/transportation_payment_description', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/transportation_payment_way', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/meals', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_cost', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_local_cost', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_default_currency', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_local_currency', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_payment_way', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_payment_description', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/transport_days_manual', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/overnights_num_manual', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/compensation_days_manual', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'compensation_decision_date', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'compensation_decision_protocol', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'compensation_petition_date', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'compensation_petition_protocol', 'usercompensationsubmitted', '*'),

    ('applications', 'update', 'CONTROLLER', 'timesheeted', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'additional_expenses', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'additional_expenses_default_currency', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'additional_expenses_description', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'participation_cost', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'participation_local_cost', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'participation_default_currency', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'participation_payment_description', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'non_grnet_quota', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/transportation_cost', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/transportation_payment_description', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/transportation_payment_way', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/meals', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_cost', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_local_cost', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_default_currency', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_local_currency', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_payment_way', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_payment_description', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/transport_days_manual', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/overnights_num_manual', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/compensation_days_manual', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'compensation_decision_date', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'compensation_decision_protocol', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'compensation_petition_date', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'compensation_petition_protocol', 'secretarycompensationsaved', '*'),

    ('applications', 'submit', 'CONTROLLER', '*', 'secretarycompensationsaved', '*'),
    ('applications', 'president_approval', 'CONTROLLER', '*', 'secretarycompensationsubmitted', '*'),
    ('applications', 'application_report', 'CONTROLLER', '*', 'secretarycompensationsubmitted', '*'),
    ('applications', 'decision_report', 'CONTROLLER', '*', 'secretarycompensationsubmitted', '*'),
    ('applications', 'cancel', 'CONTROLLER', '*', 'secretarycompensationsubmitted', '*'),

    #admin
    ('applications', 'create', 'ADMIN', '*', '*', '*'),
    ('applications', 'list', 'ADMIN', '*', '*', '*'),
    ('applications', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('applications', 'destroy', 'ADMIN', '*', '*', '*'),
    ('applications', 'submit', 'ADMIN', '*', '*', '*'),
    ('applications', 'cancel', 'ADMIN', '*', '*', '*'),
    ('applications', 'update', 'ADMIN', '*', '*', '*'),
    ('applications', 'president_approval', 'ADMIN', '*', '*', '*'),
    ('applications', 'application_report', 'ADMIN', '*', '*', '*'),
    ('applications', 'decision_report', 'ADMIN', '*', '*', '*'),


#==============================================================================


    ('petition-user-saved', 'create', 'USER', '*', '*', '*'),
    ('petition-user-saved', 'list', 'USER', '*', '*', '*'),
    ('petition-user-saved', 'retrieve', 'USER', '*', '*', '*'),
    ('petition-user-saved', 'update', 'USER', '*', '*', '*'),
    ('petition-user-saved', 'destroy', 'USER', '*', '*', '*'),
    ('petition-user-saved', 'create', 'MANAGER', '*', '*', '*'),
    ('petition-user-saved', 'list', 'MANAGER', '*', '*', '*'),
    ('petition-user-saved', 'retrieve', 'MANAGER', '*', '*', '*'),
    ('petition-user-saved', 'update', 'MANAGER', '*', '*', '*'),
    ('petition-user-saved', 'destroy', 'MANAGER', '*', '*', '*'),
    ('petition-user-saved', 'create', 'ADMIN', '*', '*', '*'),
    ('petition-user-saved', 'list', 'ADMIN', '*', '*', '*'),
    ('petition-user-saved', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('petition-user-saved', 'update', 'ADMIN', '*', '*', '*'),
    ('petition-user-saved', 'destroy', 'ADMIN', '*', '*', '*'),

    ('petition-user-submitted', 'create', 'USER', '*', '*', '*'),
    ('petition-user-submitted', 'cancel', 'USER', '*', '*', '*'),
    ('petition-user-submitted', 'list', 'USER', '*', '*', '*'),
    ('petition-user-submitted', 'retrieve', 'USER', '*', '*', '*'),
    ('petition-user-submitted', 'update', 'USER', '*', '*', '*'),
    ('petition-user-submitted', 'create', 'MANAGER', '*', '*', '*'),
    ('petition-user-submitted', 'cancel', 'MANAGER', '*', '*', '*'),
    ('petition-user-submitted', 'list', 'MANAGER', '*', '*', '*'),
    ('petition-user-submitted', 'retrieve', 'MANAGER', '*', '*', '*'),
    ('petition-user-submitted', 'update', 'MANAGER', '*', '*', '*'),
    ('petition-user-submitted', 'create', 'ADMIN', '*', '*', '*'),
    ('petition-user-submitted', 'cancel', 'ADMIN', '*', '*', '*'),
    ('petition-user-submitted', 'list', 'ADMIN', '*', '*', '*'),
    ('petition-user-submitted', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('petition-user-submitted', 'update', 'ADMIN', '*', '*', '*'),
    ('petition-user-submitted', 'list', 'VIEWER', '*', '*', '*'),
    ('petition-user-submitted', 'retrieve', 'VIEWER', '*', '*', '*'),

    ('petition-secretary-saved', 'create', 'SECRETARY', '*', '*', '*'),
    ('petition-secretary-saved', 'list', 'SECRETARY', '*', '*', '*'),
    ('petition-secretary-saved', 'retrieve', 'SECRETARY', '*', '*', '*'),
    ('petition-secretary-saved', 'update', 'SECRETARY', '*', '*', '*'),
    ('petition-secretary-saved', 'withdraw', 'SECRETARY', '*', '*', '*'),
    ('petition-secretary-saved', 'cancel_withdrawal', 'SECRETARY', '*', '*', '*'),

    ('petition-secretary-saved', 'list', 'CONTROLLER', '*', '*', '*'),
    ('petition-secretary-saved', 'retrieve', 'CONTROLLER', '*', '*', '*'),
    ('petition-secretary-saved', 'list', 'MANAGER', '*', '*', '*'),
    ('petition-secretary-saved', 'retrieve', 'MANAGER', '*', '*', '*'),
    ('petition-secretary-saved', 'update', 'MANAGER',
     'manager_movement_approval', '*', '*'),
    ('petition-secretary-saved', 'list', 'VIEWER', '*', '*', '*'),
    ('petition-secretary-saved', 'retrieve', 'VIEWER', '*', '*', '*'),


    ('petition-secretary-saved', 'create', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-saved', 'list', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-saved', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-saved', 'update', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-saved', 'get_manager_petitions', 'ADMIN', '*',
     '*', '*'),
    ('petition-secretary-saved', 'list', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('petition-secretary-saved', 'retrieve', 'PRESIDENT_SECRETARY', '*', '*', '*'),

    ('petition-secretary-submitted', 'create', 'SECRETARY', '*', '*', '*'),
    ('petition-secretary-submitted', 'list', 'SECRETARY', '*', '*', '*'),
    ('petition-secretary-submitted', 'retrieve', 'SECRETARY', '*', '*', '*'),
    ('petition-secretary-submitted', 'list', 'CONTROLLER', '*', '*', '*'),
    ('petition-secretary-submitted', 'retrieve', 'CONTROLLER', '*', '*', '*'),
    ('petition-secretary-submitted', 'update', 'SECRETARY', '*', '*', '*'),
    ('petition-secretary-submitted', 'withdraw', 'SECRETARY', '*', 'secretarysubmitted', '*'),
    ('petition-secretary-submitted', 'cancel_withdrawal', 'SECRETARY', '*', 'secretarysubmitted', '*'),

    ('petition-secretary-submitted', 'cancel', 'SECRETARY', '*', 'secretarysubmitted', '*'),
    ('petition-secretary-submitted', 'cancel', 'SECRETARY', '*', 'presidentapproved', '*'),
    ('petition-secretary-submitted', 'president_approval', 'SECRETARY', '*', '*', '*'),
    ('petition-secretary-submitted', 'cancel', 'PRESIDENT_SECRETARY', '*', 'presidentapproved', '*'),
    ('petition-secretary-submitted', 'list', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('petition-secretary-submitted', 'retrieve', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('petition-secretary-submitted', 'president_approval', 'PRESIDENT_SECRETARY', '*', '*', '*'),

    ('petition-secretary-submitted',
     'application_report', 'SECRETARY', '*', '*', '*'),
    ('petition-secretary-submitted',
     'decision_report', 'SECRETARY', '*', '*', '*'),
    ('petition-secretary-submitted', 'create', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-submitted', 'list', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-submitted', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-submitted', 'list', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-submitted', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-submitted', 'update', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-submitted', 'cancel', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-submitted',
     'president_approval', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-submitted',
     'application_report', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-submitted',
     'decision_report', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-submitted', 'list', 'VIEWER', '*', '*', '*'),
    ('petition-secretary-submitted', 'retrieve', 'VIEWER', '*', '*', '*'),

    ('petition-user-compensations', 'create', 'USER', '*', '*', '*'),
    ('petition-user-compensations', 'update', 'USER', '*', '*', '*'),
    ('petition-user-compensations', 'list', 'USER', '*', '*', '*'),
    ('petition-user-compensations', 'retrieve', 'USER', '*', '*', '*'),
    ('petition-user-compensations', 'save', 'USER', '*', '*', '*'),
    ('petition-user-compensations', 'submit', 'USER', '*', 'usercompensation', '*'),
    ('petition-user-compensations', 'cancel', 'USER', '*', '*', '*'),
    ('petition-user-compensations', 'application_report', 'USER', '*', '*',
     '*'),
    ('petition-user-compensations', 'create', 'MANAGER', '*', '*', '*'),
    ('petition-user-compensations', 'update', 'MANAGER', '*', '*', '*'),
    ('petition-user-compensations', 'list', 'MANAGER', '*', '*', '*'),
    ('petition-user-compensations', 'retrieve', 'MANAGER', '*', '*', '*'),
    ('petition-user-compensations', 'save', 'MANAGER', '*', '*', '*'),
    ('petition-user-compensations', 'submit', 'MANAGER', '*', 'usercompensation', '*'),
    ('petition-user-compensations', 'cancel', 'MANAGER', '*', '*', '*'),
    ('petition-user-compensations', 'application_report', 'MANAGER', '*', '*',
     '*'),
    ('petition-user-compensations', 'create', 'ADMIN', '*', '*', '*'),
    ('petition-user-compensations', 'update', 'ADMIN', '*', '*', '*'),
    ('petition-user-compensations', 'list', 'ADMIN', '*', '*', '*'),
    ('petition-user-compensations', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('petition-user-compensations', 'save', 'ADMIN', '*', '*', '*'),
    ('petition-user-compensations', 'submit', 'ADMIN', '*', 'usercompensation', '*'),
    ('petition-user-compensations', 'cancel', 'ADMIN', '*', '*', '*'),
    ('petition-user-compensations', 'application_report', 'ADMIN', '*', '*',
     '*'),
    ('petition-user-compensations', 'list', 'VIEWER', '*', '*', '*'),
    ('petition-user-compensations', 'retrieve', 'VIEWER', '*', '*', '*'),


    ('petition-secretary-compensations', 'create', 'CONTROLLER', '*', '*', '*'),
    ('petition-secretary-compensations', 'list', 'CONTROLLER', '*', '*', '*'),
    ('petition-secretary-compensations', 'retrieve', 'CONTROLLER', '*', '*', '*'),
    ('petition-secretary-compensations', 'update', 'CONTROLLER', '*', '*', '*'),
    ('petition-secretary-compensations', 'cancel', 'CONTROLLER', '*', 'secretarycompensationsubmitted', '*'),
    ('petition-secretary-compensations', 'cancel', 'CONTROLLER', '*', 'presidentcompensationapproved', '*'),
    ('petition-secretary-compensations', 'president_approval', 'CONTROLLER', '*', '*', '*'),
    ('petition-secretary-compensations', 'application_report', 'CONTROLLER', '*', '*', '*'),
    ('petition-secretary-compensations', 'decision_report', 'CONTROLLER', '*', '*', '*'),
    ('petition-secretary-compensations', 'save', 'CONTROLLER', '*', '*', '*'),
    ('petition-secretary-compensations', 'submit', 'CONTROLLER', '*', '*', '*'),
    ('petition-secretary-compensations', 'create', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-compensations', 'list', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-compensations', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-compensations', 'update', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-compensations', 'cancel', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-compensations', 'president_approval', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-compensations', 'application_report', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-compensations', 'decision_report', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-compensations', 'save', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-compensations', 'submit', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-compensations', 'cancel_withdrawal', 'CONTROLLER', '*', '*', '*'),
    ('petition-secretary-compensations', 'cancel_withdrawal', 'ADMIN', '*', '*', '*'),

    ('petition-secretary-compensations', 'list', 'SECRETARY', '*', '*', '*'),
    ('petition-secretary-compensations', 'retrieve', 'SECRETARY', '*', '*', '*'),
    ('petition-secretary-compensations', 'update', 'SECRETARY', '*', '*', '*'),
    ('petition-secretary-compensations', 'cancel', 'SECRETARY', '*', '*', '*'),
    ('petition-secretary-compensations', 'list', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-compensations', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-compensations', 'update', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-compensations', 'cancel', 'ADMIN', '*', '*', '*'),
    ('petition-secretary-compensations', 'list', 'VIEWER', '*', '*', '*'),
    ('petition-secretary-compensations', 'retrieve', 'VIEWER', '*', '*', '*'),

]
