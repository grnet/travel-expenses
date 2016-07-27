export const UIS = {
  "petition_user": {
    fieldsets: [
      {
        'label': 'User data',
        'text': 'This is the fieldset help text',
        'fields': ['first_name', 'last_name', 'specialty', 'kind', 'tax_reg_num', 'tax_office', 'iban', 'user_category']
      },
      {
        'label': 'Travel Data',
        'fields': ['dse', 'project', 'reason', 'movement_category', 'departure_point', 'arrival_point',
        'task_start_date', 'task_end_date', 'depart_date', 'return_date', 'mean_of_transport', 'transportation',
        'accomondation', 'registration_cost', 'additional_expenses', 'meals', 'non_grnet_quota', 'user_recommendation']
      },
    ],
    layout: {
      flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
    }
  },
  "petition_travel": {
    layoutMap: {"reason": 100},
    fieldsets: [
      {
        'label': 'User data',
        'fields': ['first_name', 'last_name', 'specialty', 'kind', 'tax_reg_num', 'tax_office', 'iban', 'category']
      },
      {
        'label': 'Travel Data',
        'fields': ['dse', 'project', 'reason', 'movement_category', 'departure_point', 'arrival_point',
        'task_start_date', 'task_end_date', 'depart_date', 'return_date', 'mean_of_transport', 'transportation',
        'accomondation', 'registration_cost', 'additional_expenses', 'meals', 'non_grnet_quota', 'user_recommendation']
      },
      {
        'label': 'Secretary Data',
        'fields': ['movement_num', 'expenditure_date_protocol',
        'expenditure_protocol', 'movement_date_protocol', 'movement_protocol', 'trip_days_before']
      },
      {
        'label': 'Computed Data',
        'fields': ['transport_days_manual', 'transport_days_proposed', 'overnights_num_manual',
        'overnights_num_proposed', 'compensation_days_manual', 'compensation_days_proposed', 'same_day_return_task', 
        'trip_days_before', 'trip_days_after', 'overnights_sum_cost', 'compensation_level', 'compensation_final', 'total_cost']
      },
    ],
    layout: {
      flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
    }
  }
};
