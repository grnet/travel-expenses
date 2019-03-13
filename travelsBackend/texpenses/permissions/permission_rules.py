PERMISSION_RULES = [
    ('tax-office', 'list', 'ADMIN', '*', '*', '*'),
    ('tax-office', 'list', 'anonymous', '*', '*', '*'),
    ('tax-office', 'list', 'USER', '*', '*', '*'),
    ('tax-office', 'list', 'SECRETARY', '*', '*', '*'),
    ('tax-office', 'list', 'CONTROLLER', '*', '*', '*'),
    ('tax-office', 'list', 'MANAGER', '*', '*', '*'),
    ('tax-office', 'list', 'VIEWER', '*', '*', '*'),
    ('tax-office', 'list', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('tax-office', 'list', 'HELPDESK', '*', '*', '*'),
    ('tax-office', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('tax-office', 'retrieve', 'anonymous', '*', '*', '*'),
    ('tax-office', 'retrieve', 'USER', '*', '*', '*'),
    ('tax-office', 'retrieve', 'SECRETARY', '*', '*', '*'),
    ('tax-office', 'retrieve', 'CONTROLLER', '*', '*', '*'),
    ('tax-office', 'retrieve', 'MANAGER', '*', '*', '*'),
    ('tax-office', 'retrieve', 'VIEWER', '*', '*', '*'),
    ('tax-office', 'retrieve', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('tax-office', 'retrieve', 'HELPDESK', '*', '*', '*'),


    ('project', 'list', 'ADMIN', '*', '*', '*'),
    ('project', 'list', 'anonymous', '*', '*', '*'),
    ('project', 'list', 'USER', '*', '*', '*'),
    ('project', 'list', 'SECRETARY', '*', '*', '*'),
    ('project', 'list', 'CONTROLLER', '*', '*', '*'),
    ('project', 'list', 'MANAGER', '*', '*', '*'),
    ('project', 'list', 'VIEWER', '*', '*', '*'),
    ('project', 'list', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('project', 'list', 'HELPDESK', '*', '*', '*'),
    ('project', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('project', 'retrieve', 'anonymous', '*', '*', '*'),
    ('project', 'retrieve', 'USER', '*', '*', '*'),
    ('project', 'retrieve', 'SECRETARY', '*', '*', '*'),
    ('project', 'retrieve', 'CONTROLLER', '*', '*', '*'),
    ('project', 'retrieve', 'MANAGER', '*', '*', '*'),
    ('project', 'retrieve', 'VIEWER', '*', '*', '*'),
    ('project', 'retrieve', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('project', 'retrieve', 'HELPDESK', '*', '*', '*'),
    ('project', 'create', 'ADMIN', '*', '*', '*'),
    ('project', 'create', 'HELPDESK', '*', '*', '*'),
    ('project', 'update', 'ADMIN', '*', '*', '*'),
    ('project', 'update', 'HELPDESK', '*', '*', '*'),
    ('project', 'stats', 'ADMIN', '*', '*', '*'),
    ('project', 'stats', 'CONTROLLER', '*', '*', '*'),
    ('project', 'stats', 'HELPDESK', '*', '*', '*'),
    ('project', 'toggle_active', 'ADMIN', '*', '*', '*'),
    ('project', 'toggle_active', 'HELPDESK', '*', '*', '*'),

    ('countries', 'list', 'ADMIN', '*', '*', '*'),
    ('countries', 'list', 'anonymous', '*', '*', '*'),
    ('countries', 'list', 'USER', '*', '*', '*'),
    ('countries', 'list', 'SECRETARY', '*', '*', '*'),
    ('countries', 'list', 'CONTROLLER', '*', '*', '*'),
    ('countries', 'list', 'MANAGER', '*', '*', '*'),
    ('countries', 'list', 'VIEWER', '*', '*', '*'),
    ('countries', 'list', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('countries', 'list', 'HELPDESK', '*', '*', '*'),
    ('countries', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('countries', 'retrieve', 'anonymous', '*', '*', '*'),
    ('countries', 'retrieve', 'USER', '*', '*', '*'),
    ('countries', 'retrieve', 'SECRETARY', '*', '*', '*'),
    ('countries', 'retrieve', 'CONTROLLER', '*', '*', '*'),
    ('countries', 'retrieve', 'MANAGER', '*', '*', '*'),
    ('countries', 'retrieve', 'VIEWER', '*', '*', '*'),
    ('countries', 'retrieve', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('countries', 'retrieve', 'HELPDESK', '*', '*', '*'),

    ('city', 'list', 'ADMIN', '*', '*', '*'),
    ('city', 'list', 'anonymous', '*', '*', '*'),
    ('city', 'list', 'USER', '*', '*', '*'),
    ('city', 'list', 'SECRETARY', '*', '*', '*'),
    ('city', 'list', 'CONTROLLER', '*', '*', '*'),
    ('city', 'list', 'MANAGER', '*', '*', '*'),
    ('city', 'list', 'VIEWER', '*', '*', '*'),
    ('city', 'list', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('city', 'list', 'HELPDESK', '*', '*', '*'),
    ('city', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('city', 'retrieve', 'anonymous', '*', '*', '*'),
    ('city', 'retrieve', 'USER', '*', '*', '*'),
    ('city', 'retrieve', 'SECRETARY', '*', '*', '*'),
    ('city', 'retrieve', 'CONTROLLER', '*', '*', '*'),
    ('city', 'retrieve', 'MANAGER', '*', '*', '*'),
    ('city', 'retrieve', 'VIEWER', '*', '*', '*'),
    ('city', 'retrieve', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('city', 'retrieve', 'HELPDESK', '*', '*', '*'),

    ('users', 'list', 'ADMIN', '*', '*', '*'),
    ('users', 'list', 'HELPDESK', '*', '*', '*'),
    ('users', 'retrieve', 'USER', '*', 'isme', '*'),
    ('users', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('users', 'retrieve', 'SECRETARY', '*', 'isme', '*'),
    ('users', 'retrieve', 'CONTROLLER', '*', 'isme', '*'),
    ('users', 'retrieve', 'MANAGER', '*', 'isme', '*'),
    ('users', 'retrieve', 'VIEWER', '*', 'isme', '*'),
    ('users', 'retrieve', 'PRESIDENT_SECRETARY', '*', 'isme', '*'),
    ('users', 'retrieve', 'HELPDESK', '*', '*', '*'),
    ('users', 'update', 'ADMIN', 'email', '*', '*'),
    ('users', 'update', 'HELPDESK', 'email', '*', '*'),
    ('users', 'toggle_active', 'ADMIN', '*', '*', '*'),
    ('users', 'toggle_active', 'HELPDESK', '*', '*', '*'),

#==============================================================================

    # user
    ('applications', 'create', 'USER', '*', '*', '*'),
    ('applications', 'list', 'USER', '*', '*', '*'),
    ('applications', 'retrieve', 'USER', '*', '*', '*'),
    ('applications', 'mark_as_deleted', 'USER', '*', 'ownedusersaved', '*'),
    ('applications', 'submit', 'USER', '*', 'ownedusersaved', '*'),
    ('applications', 'submit', 'USER', '*', 'ownedusercompensationsaved', '*'),

    ('applications', 'cancel', 'USER', '*', 'ownedusersubmitted', '*'),
    ('applications', 'cancel', 'USER', '*', 'ownedusercompensationsubmitted', '*'),

    ('applications', 'application_report', 'USER', '*', 'ownedusercompensationsaved', '*'),
    ('applications', 'application_report', 'USER', '*', 'ownedpresidentapproved', '*'),

    ('applications', 'update', 'USER', 'project', 'ownedusersaved', '*'),
    ('applications', 'update', 'USER', 'reason', 'ownedusersaved', '*'),
    ('applications', 'update', 'USER', 'task_start_date', 'ownedusersaved', '*'),
    ('applications', 'update', 'USER', 'task_end_date', 'ownedusersaved', '*'),
    ('applications', 'update', 'USER', 'participation_cost', 'ownedusersaved', '*'),
    ('applications', 'update', 'USER', 'participation_local_cost', 'ownedusersaved', '*'),
    ('applications', 'update', 'USER', 'participation_local_currency', 'ownedusersaved', '*'),
    ('applications', 'update', 'USER', 'user_recommendation', 'ownedusersaved', '*'),
    ('applications', 'update', 'USER', 'travel_info/departure_point','ownedusersaved', '*'),
    ('applications', 'update', 'USER', 'travel_info/arrival_point','ownedusersaved', '*'),
    ('applications', 'update', 'USER', 'travel_info/depart_date','ownedusersaved', '*'),
    ('applications', 'update', 'USER', 'travel_info/return_date','ownedusersaved', '*'),

    ('applications', 'update', 'USER', 'travel_info/departure_point','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'USER', 'travel_info/arrival_point','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'USER', 'travel_info/depart_date','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'USER', 'travel_info/return_date','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'USER', 'travel_files','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'USER', 'travel_report','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'USER', 'additional_expenses','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'USER', 'additional_expenses_local_currency','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'USER', 'additional_expenses_default_currency','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'USER', 'additional_expenses_description','ownedusercompensationsaved', '*'),

    ('applications', 'update', 'USER', 'travel_info/departure_point','ownedpresidentapproved', '*'),
    ('applications', 'update', 'USER', 'travel_info/arrival_point','ownedpresidentapproved', '*'),
    ('applications', 'update', 'USER', 'travel_info/depart_date','ownedpresidentapproved', '*'),
    ('applications', 'update', 'USER', 'travel_info/return_date','ownedpresidentapproved', '*'),
    ('applications', 'update', 'USER', 'travel_files','ownedpresidentapproved', '*'),
    ('applications', 'update', 'USER', 'travel_report','ownedpresidentapproved', '*'),
    ('applications', 'update', 'USER', 'additional_expenses','ownedpresidentapproved', '*'),
    ('applications', 'update', 'USER', 'additional_expenses_local_currency','ownedpresidentapproved', '*'),
    ('applications', 'update', 'USER', 'additional_expenses_default_currency','ownedpresidentapproved', '*'),
    ('applications', 'update', 'USER', 'additional_expenses_description','ownedpresidentapproved', '*'),

    # viewer
    ('applications', 'list', 'VIEWER', '*','*', '*'),
    ('applications', 'retrieve', 'VIEWER', '*','*','*'),

    #manager
    ('applications', 'create', 'MANAGER', '*', '*', '*'),
    ('applications', 'list', 'MANAGER', '*', '*', '*'),
    ('applications', 'update_manager_movement_approval', 'MANAGER', '*', 'usersubmitted', '*'),
    ('applications', 'update_manager_movement_approval', 'MANAGER', '*', 'secretarysaved', '*'),
    ('applications', 'application_report', 'MANAGER', '*', 'usercompensationsaved', '*'),
    ('applications', 'application_report', 'MANAGER', '*', 'presidentapproved', '*'),

    ('applications', 'retrieve', 'MANAGER', '*', '*', '*'),
    ('applications', 'mark_as_deleted', 'MANAGER', '*', 'ownedusersaved', '*'),
    ('applications', 'submit', 'MANAGER', '*', 'ownedusersaved', '*'),
    ('applications', 'submit', 'MANAGER', '*', 'ownedusercompensationsaved', '*'),
    ('applications', 'cancel', 'MANAGER', '*',  'ownedusersubmitted', '*'),
    ('applications', 'cancel', 'MANAGER', '*', 'ownedusercompensationsubmitted', '*'),

    ('applications', 'update', 'MANAGER', 'project', 'ownedusersaved', '*'),
    ('applications', 'update', 'MANAGER', 'reason', 'ownedusersaved', '*'),
    ('applications', 'update', 'MANAGER', 'task_start_date', 'ownedusersaved', '*'),
    ('applications', 'update', 'MANAGER', 'task_end_date', 'ownedusersaved', '*'),
    ('applications', 'update', 'MANAGER', 'participation_cost', 'ownedusersaved', '*'),
    ('applications', 'update', 'MANAGER', 'participation_local_cost', 'ownedusersaved', '*'),
    ('applications', 'update', 'MANAGER', 'participation_local_currency', 'ownedusersaved', '*'),
    ('applications', 'update', 'MANAGER', 'user_recommendation', 'ownedusersaved','*'),
    ('applications', 'update', 'MANAGER', 'travel_info/departure_point','ownedusersaved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/arrival_point','ownedusersaved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/depart_date','ownedusersaved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/return_date','ownedusersaved', '*'),

    ('applications', 'update', 'MANAGER', 'travel_info/departure_point','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/arrival_point','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/depart_date','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/return_date','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_files','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_report','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'MANAGER', 'additional_expenses','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'MANAGER', 'additional_expenses_local_currency','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'MANAGER', 'additional_expenses_default_currency','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'MANAGER', 'additional_expenses_description','ownedusercompensationsaved', '*'),

    ('applications', 'update', 'MANAGER', 'travel_info/departure_point','ownedpresidentapproved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/arrival_point','ownedpresidentapproved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/depart_date','ownedpresidentapproved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_info/return_date','ownedpresidentapproved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_files','ownedpresidentapproved', '*'),
    ('applications', 'update', 'MANAGER', 'travel_report','ownedpresidentapproved', '*'),
    ('applications', 'update', 'MANAGER', 'additional_expenses','ownedpresidentapproved', '*'),
    ('applications', 'update', 'MANAGER', 'additional_expenses_local_currency','ownedpresidentapproved', '*'),
    ('applications', 'update', 'MANAGER', 'additional_expenses_default_currency','ownedpresidentapproved', '*'),
    ('applications', 'update', 'MANAGER', 'additional_expenses_description','ownedpresidentapproved', '*'),

     #secretary
    ('applications', 'list', 'SECRETARY', '*','*','*'),
    ('applications', 'retrieve', 'SECRETARY', '*','*','*'),
    ('applications', 'update', 'SECRETARY', 'project', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'dse', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'reason', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'task_start_date', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'task_end_date', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'participation_cost', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'participation_local_cost', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'participation_local_currency', 'secretarysaved', '*'),
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
    ('applications', 'update', 'SECRETARY', 'travel_info/transportation_payment_way', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/means_of_transport', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/transportation_cost', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/no_transportation_calculation', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/transportation_payment_description', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/meals', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_cost', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_total_cost', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_default_currency', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_local_cost', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_total_local_cost', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_local_currency', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_payment_way', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/accommodation_payment_description', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/transport_days_manual', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/overnights_num_manual', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/compensation_days_manual', 'secretarysaved', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/distance', 'secretarysaved', '*'),
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
    ('applications', 'update', 'SECRETARY', 'participation_local_cost', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'participation_local_currency', 'usersubmitted', '*'),
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
    ('applications', 'update', 'SECRETARY', 'travel_info/transportation_payment_way', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/means_of_transport', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/transportation_cost', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'travel_info/no_transportation_calculation', 'usersubmitted', '*'),
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
    ('applications', 'update', 'SECRETARY', 'travel_info/distance', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'movement_id', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'movement_date_protocol', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'movement_protocol', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'expenditure_protocol', 'usersubmitted', '*'),
    ('applications', 'update', 'SECRETARY', 'expenditure_date_protocol', 'usersubmitted', '*'),

    ('applications', 'submit', 'SECRETARY', '*', 'secretarysaved', '*'),
    ('applications', 'president_approval', 'SECRETARY', '*', 'secretarysubmitted', '*'),
    ('applications', 'president_approval', 'SECRETARY', '*', 'secretarycompensationsubmitted', '*'),
    ('applications', 'application_report', 'SECRETARY', '*', 'secretarysubmitted', '*'),
    ('applications', 'decision_report', 'SECRETARY', '*', 'secretarysubmitted', '*'),
    ('applications', 'cancel', 'SECRETARY', '*', 'secretarysubmitted', '*'),
    ('applications', 'cancel', 'SECRETARY', '*', 'presidentapproved', '*'),
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
    ('applications', 'update', 'CONTROLLER', 'task_start_date', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'task_end_date', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'additional_expenses', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'additional_expenses_default_currency', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'additional_expenses_description', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'additional_expenses_grnet', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'participation_cost', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'participation_local_cost', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'participation_local_currency', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'participation_default_currency', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'non_grnet_quota', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/depart_date', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/return_date', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/transportation_cost', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/no_transportation_calculation', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/transportation_payment_way', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/means_of_transport', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/meals', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_cost', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_total_cost', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_local_cost', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_total_local_cost', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_default_currency', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_local_currency', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_payment_way', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/transport_days_manual', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/overnights_num_manual', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/compensation_days_manual', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/distance', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'compensation_decision_date', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'compensation_decision_protocol', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'compensation_petition_date', 'usercompensationsubmitted', '*'),
    ('applications', 'update', 'CONTROLLER', 'compensation_petition_protocol', 'usercompensationsubmitted', '*'),

    ('applications', 'update_timesheeted', 'CONTROLLER', '*', 'secretarycompensationsaved', '*'),
    ('applications', 'update_timesheeted', 'CONTROLLER', '*', 'secretarycompensationsubmitted', '*'),
    ('applications', 'update_timesheeted', 'CONTROLLER', '*', 'presidentcompensationapproved', '*'),
    ('applications', 'update', 'CONTROLLER', 'task_start_date', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'task_end_date', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'additional_expenses', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'additional_expenses_local_currency', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'additional_expenses_default_currency', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'additional_expenses_description', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'additional_expenses_grnet', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'participation_cost', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'participation_local_cost', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'participation_local_currency', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'participation_default_currency', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'non_grnet_quota', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/depart_date', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/return_date', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/transportation_cost', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/no_transportation_calculation', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/transportation_payment_way', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/means_of_transport', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/meals', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_cost', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_total_cost', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_local_cost', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_total_local_cost', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_default_currency', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_local_currency', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/accommodation_payment_way', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/transport_days_manual', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/overnights_num_manual', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/compensation_days_manual', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'travel_info/distance', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'compensation_decision_date', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'compensation_decision_protocol', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'compensation_petition_date', 'secretarycompensationsaved', '*'),
    ('applications', 'update', 'CONTROLLER', 'compensation_petition_protocol', 'secretarycompensationsaved', '*'),

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
    ('applications', 'mark_as_deleted', 'ADMIN', '*', '*', '*'),
    ('applications', 'submit', 'ADMIN', '*', '*', '*'),
    ('applications', 'cancel', 'ADMIN', '*', '*', '*'),
    ('applications', 'update', 'ADMIN', '*', '*', '*'),
    ('applications', 'president_approval', 'ADMIN', '*', '*', '*'),
    ('applications', 'application_report', 'ADMIN', '*', '*', '*'),
    ('applications', 'decision_report', 'ADMIN', '*', '*', '*'),
    ('applications', 'cancel_withdrawal', 'ADMIN', '*', '*', '*'),
    ('applications', 'reset', 'ADMIN', '*', '*', '*'),

    #helpdesk
    ('applications', 'reset', 'HELPDESK', '*', '*', '*'),
    ('applications', 'create', 'HELPDESK', '*', '*', '*'),
    ('applications', 'list', 'HELPDESK', '*', '*', '*'),
    ('applications', 'retrieve', 'HELPDESK', '*', '*', '*'),
    ('applications', 'mark_as_deleted', 'HELPDESK', '*', 'ownedusersaved', '*'),
    ('applications', 'submit', 'HELPDESK', '*', 'ownedusersaved', '*'),
    ('applications', 'submit', 'HELPDESK', '*', 'ownedusercompensationsaved', '*'),

    ('applications', 'cancel', 'HELPDESK', '*', 'ownedusersubmitted', '*'),
    ('applications', 'cancel', 'HELPDESK', '*', 'ownedusercompensationsubmitted', '*'),

    ('applications', 'application_report', 'HELPDESK', '*', 'ownedusercompensationsaved', '*'),
    ('applications', 'application_report', 'HELPDESK', '*', 'ownedpresidentapproved', '*'),

    ('applications', 'update', 'HELPDESK', 'project', 'ownedusersaved', '*'),
    ('applications', 'update', 'HELPDESK', 'reason', 'ownedusersaved', '*'),
    ('applications', 'update', 'HELPDESK', 'task_start_date', 'ownedusersaved', '*'),
    ('applications', 'update', 'HELPDESK', 'task_end_date', 'ownedusersaved', '*'),
    ('applications', 'update', 'HELPDESK', 'participation_cost', 'ownedusersaved', '*'),
    ('applications', 'update', 'HELPDESK', 'participation_local_cost', 'ownedusersaved', '*'),
    ('applications', 'update', 'HELPDESK', 'participation_local_currency', 'ownedusersaved', '*'),
    ('applications', 'update', 'HELPDESK', 'user_recommendation', 'ownedusersaved', '*'),
    ('applications', 'update', 'HELPDESK', 'travel_info/departure_point','ownedusersaved', '*'),
    ('applications', 'update', 'HELPDESK', 'travel_info/arrival_point','ownedusersaved', '*'),
    ('applications', 'update', 'HELPDESK', 'travel_info/depart_date','ownedusersaved', '*'),
    ('applications', 'update', 'HELPDESK', 'travel_info/return_date','ownedusersaved', '*'),

    ('applications', 'update', 'HELPDESK', 'travel_info/departure_point','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'HELPDESK', 'travel_info/arrival_point','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'HELPDESK', 'travel_info/depart_date','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'HELPDESK', 'travel_info/return_date','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'HELPDESK', 'travel_files','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'HELPDESK', 'travel_report','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'HELPDESK', 'additional_expenses','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'HELPDESK', 'additional_expenses_local_currency','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'HELPDESK', 'additional_expenses_default_currency','ownedusercompensationsaved', '*'),
    ('applications', 'update', 'HELPDESK', 'additional_expenses_description','ownedusercompensationsaved', '*'),

    ('applications', 'update', 'HELPDESK', 'travel_info/departure_point','ownedpresidentapproved', '*'),
    ('applications', 'update', 'HELPDESK', 'travel_info/arrival_point','ownedpresidentapproved', '*'),
    ('applications', 'update', 'HELPDESK', 'travel_info/depart_date','ownedpresidentapproved', '*'),
    ('applications', 'update', 'HELPDESK', 'travel_info/return_date','ownedpresidentapproved', '*'),
    ('applications', 'update', 'HELPDESK', 'travel_files','ownedpresidentapproved', '*'),
    ('applications', 'update', 'HELPDESK', 'travel_report','ownedpresidentapproved', '*'),
    ('applications', 'update', 'HELPDESK', 'additional_expenses','ownedpresidentapproved', '*'),
    ('applications', 'update', 'HELPDESK', 'additional_expenses_local_currency','ownedpresidentapproved', '*'),
    ('applications', 'update', 'HELPDESK', 'additional_expenses_default_currency','ownedpresidentapproved', '*'),
    ('applications', 'update', 'HELPDESK', 'additional_expenses_description','ownedpresidentapproved', '*'),

    #president-secretary
    ('applications', 'cancel', 'PRESIDENT_SECRETARY', '*', 'presidentapproved', '*'),
    ('applications', 'cancel', 'PRESIDENT_SECRETARY', '*', 'presidentcompensationapproved', '*'),
    ('applications', 'president_approval', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('applications', 'list', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('applications', 'retrieve', 'PRESIDENT_SECRETARY', '*', '*', '*'),

    ('city-distances', 'list', 'ADMIN', '*', '*', '*'),
    ('city-distances', 'list', 'anonymous', '*', '*', '*'),
    ('city-distances', 'list', 'USER', '*', '*', '*'),
    ('city-distances', 'list', 'SECRETARY', '*', '*', '*'),
    ('city-distances', 'list', 'CONTROLLER', '*', '*', '*'),
    ('city-distances', 'list', 'MANAGER', '*', '*', '*'),
    ('city-distances', 'list', 'VIEWER', '*', '*', '*'),
    ('city-distances', 'list', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('city-distances', 'list', 'HELPDESK', '*', '*', '*'),
    ('city-distances', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('city-distances', 'retrieve', 'anonymous', '*', '*', '*'),
    ('city-distances', 'retrieve', 'USER', '*', '*', '*'),
    ('city-distances', 'retrieve', 'SECRETARY', '*', '*', '*'),
    ('city-distances', 'retrieve', 'CONTROLLER', '*', '*', '*'),
    ('city-distances', 'retrieve', 'MANAGER', '*', '*', '*'),
    ('city-distances', 'retrieve', 'VIEWER', '*', '*', '*'),
    ('city-distances', 'retrieve', 'PRESIDENT_SECRETARY', '*', '*', '*'),
    ('city-distances', 'retrieve', 'HELPDESK', '*', '*', '*'),
    ('city-distances', 'create', 'ADMIN', '*', '*', '*'),
    ('city-distances', 'create', 'HELPDESK', '*', '*', '*'),
    ('city-distances', 'update', 'ADMIN', '*', '*', '*'),
    ('city-distances', 'update', 'HELPDESK', '*', '*', '*'),

    ('travel-files', 'list', 'ADMIN', '*', '*', '*'),
    ('travel-files', 'list', 'HELPDESK', '*', '*', '*'),
    ('travel-files', 'retrieve', 'ADMIN', '*', '*', '*'),
    ('travel-files', 'retrieve', 'USER', '*', '*', '*'),
    ('travel-files', 'retrieve', 'SECRETARY', '*', '*', '*'),
    ('travel-files', 'retrieve', 'CONTROLLER', '*', '*', '*'),
    ('travel-files', 'retrieve', 'MANAGER', '*', '*', '*'),
    ('travel-files', 'retrieve', 'VIEWER', '*', '*', '*'),
    ('travel-files', 'retrieve', 'HELPDESK', '*', '*', '*'),
    ('travel-files', 'download_head', 'ADMIN', '*', '*', ''),
    ('travel-files', 'download_head', 'USER', '*', 'owned', ''),
    ('travel-files', 'download_head', 'HELPDESK', '*', '*', ''),
    ('travel-files', 'download_head', 'SECRETARY', '*', '*', ''),
    ('travel-files', 'download_head', 'CONTROLLER', '*', '*', ''),
    ('travel-files', 'download_head', 'MANAGER', '*', '*', ''),
    ('travel-files', 'download_get', '*', '*', '*', ''),
    ('travel-files', 'destroy', 'USER', '*', 'owned', ''),
    ('applications', 'upload', 'USER', '*', '*', '*'),
    ('applications', 'upload', 'MANAGER', '*', '*', '*'),
]
