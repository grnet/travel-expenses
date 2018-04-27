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
    ('applications', 'cancel', 'MANAGER', '*',  'usersubmitted', '*'),
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
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_total_cost', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_default_currency', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_local_cost', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_total_local_cost', 'secretarysaved', '*'),
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
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_total_cost', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_default_currency', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_local_cost', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_total_local_cost', 'usersubmitted', '*'),
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
    ('applications', 'cancel', 'SECRETARY', '*', 'presidentapproved', '*'),
    ('applications', 'president_approval', 'SECRETARY', '*', '*', '*'),
    ('applications', 'withdraw', 'SECRETARY', '*', 'secretarysaved', '*'),
    ('applications', 'withdraw', 'SECRETARY', '*', 'secretarysubmitted', '*'),
    ('applications', 'cancel_withdrawal', 'SECRETARY', '*', 'secretarysaved', '*'),
    ('applications', 'cancel_withdrawal', 'SECRETARY', '*', 'secretarysubmitted', '*'),

    #controller
    ('applications', 'list', 'CONTROLLER', '*','*','*'),
    ('applications', 'retrieve', 'CONTROLLER', '*','*','*'),
    ('applications', 'update_timesheeted', 'CONTROLLER', '*', 'presidentapproved', '*'),
    ('applications', 'update_timesheeted', 'CONTROLLER', '*', 'usercompensationsaved', '*'),
    ('applications', 'update_timesheeted', 'CONTROLLER', '*', 'usercompensationsubmitted', '*'),
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
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_total_cost', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_local_cost', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_total_local_cost', 'usercompensationsubmitted', '*'),
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

    ('applications', 'update_timesheeted', 'CONTROLLER', '*', 'secretarycompensationsaved', '*'),
    ('applications', 'update_timesheeted', 'CONTROLLER', '*', 'secretarycompensationsubmitted', '*'),
    ('applications', 'update_timesheeted', 'CONTROLLER', '*', 'presidentcompensationapproved', '*'),
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
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_total_cost', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_local_cost', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_total_local_cost', 'secretarycompensationsaved', '*'),
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
    ('applications', 'update', 'CONTROLLER', 'total_cost_manual', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'total_cost_manual', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'total_cost_change_reason', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'total_cost_change_reason', 'secretarycompensationsaved', '*'),

    ('applications', 'submit', 'CONTROLLER', '*', 'secretarycompensationsaved', '*'),
    ('applications', 'president_approval', 'CONTROLLER', '*', 'secretarycompensationsubmitted', '*'),
    ('applications', 'application_report', 'CONTROLLER', '*', 'secretarycompensationsubmitted', '*'),
    ('applications', 'decision_report', 'CONTROLLER', '*', 'secretarycompensationsubmitted', '*'),
    ('applications', 'cancel', 'CONTROLLER', '*', 'secretarycompensationsubmitted', '*'),
    ('applications', 'cancel', 'CONTROLLER', '*', 'presidentcompensationapproved', '*'),
    ('applications', 'withdraw', 'CONTROLLER', '*', 'secretarycompensationsaved', '*'),
    ('applications', 'withdraw', 'CONTROLLER', '*', 'secretarycompensationsubmitted', '*'),
    ('applications', 'cancel_withdrawal', 'CONTROLLER', '*', '*', '*'),

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
    ('applications', 'cancel_withdrawal', 'ADMIN', '*', '*', '*'),

    #president-secretary
    ('applications', 'cancel', 'PRESIDENT_SECRETARY', '*', 'presidentapproved', '*'),
    ('applications', 'cancel', 'PRESIDENT_SECRETARY', '*', 'presidentcompensationapproved', '*'),
    ('applications', 'president_approval', 'PRESIDENT_SECRETARY', '*', 'secretarysubmitted', '*'),
    ('applications', 'list', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('applications', 'retrieve', 'PRESIDENT_SECRETARY', '*', '*', '*'),
]
