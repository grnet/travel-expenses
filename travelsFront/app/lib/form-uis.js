export const UIS = {
  "petition_user": {
    layoutMap: {"reason": 100},
    fieldsets: [
      {
        'label': 'Profile',
        'fields': ['name', 'surname', 'specialtyID', 
        'kind', 'taxRegNum', 'taxOffice', 'iban', 'user_category']
      },
      {
        'label': 'Travel Data',
        'fields': ['project', 'reason', 'movementCategories',  'departurePoint', 'arrivalPoint',
        'taskStartDate', 'taskEndDate', 'depart_date', 'return_date', 'transportation', 
        'recCostParticipation', 'additional_expenses_initial', 'additional_expenses_initial_description']
      },
    ],
    layout: {
      flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
    }
  },
  "petition_travel": {
    layoutMap: {"reason": 100},
    fieldsets: [
      {
        'label': 'Profile',
        'fields': ['name', 'surname', 'specialtyID', 
        'kind', 'taxRegNum', 'taxOffice', 'iban', 'user_category']
      },
      {
        'label': 'Travel Data',
        'fields': ['dse', 'project', 'reason', 'movementCategory', 'departurePoint', 'arrivalPoint',
        'taskStartDate', 'taskEndDate', 'depart_date', 'return_date', 'transportation', 'flight',
        'accomondation', 'recCostParticipation', 'additional_expenses_initial', 'feeding', 'non_grnet_quota']
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
}
