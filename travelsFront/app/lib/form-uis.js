export const UIS = {
  "petition_user": {
    fieldsets: [
      {
        'label': 'user_data.label',
        'fields': ['first_name', 'last_name', 'specialty', 'kind', 'tax_reg_num', 'tax_office', 'iban', 'user_category']
      },
      {
        'label': 'travel_data.label',
        'fields': ['dse', 'project', 'reason', 'departure_point', 'arrival_point','movement_category', 'country_category',
        'task_start_date', 'task_end_date', 'depart_date', 'return_date', 'means_of_transport', 'transportation_cost', 'meals',
        'accommodation_local_cost', 'accommodation_local_currency', 'additional_expenses_initial', 'participation_local_cost', 
        'participation_local_currency', 'additional_expenses_initial_description', 'user_recommendation']
      },
    ],
    layout: {
      flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 100, 50, 50, 50, 50, 50, 50, 50, 30, 20, 50, 100, 100, 50, 50, 50, 50, 50, 50, 50, 50, 30, 20]
    }
  },
  "petition_travel": {
    layoutMap: {"reason": 100},
    fieldsets: [
      {
        'label': 'user_data.label',
        'fields': ['first_name', 'last_name', 'specialty', 'kind', 'tax_reg_num', 'tax_office', 'iban', 'user_category']
      },
      {
        'label': 'travel_data.label',
        'fields': ['dse', 'project', 'reason', 'departure_point', 'arrival_point','movement_category', 'country_category',
        'task_start_date', 'task_end_date', 'depart_date', 'return_date', 'means_of_transport', 'transportation_cost',
        'transportation_payment_way', 'transportation_payment_description', 'meals', 'accommodation_local_cost', 
        'accommodation_local_currency', 'accommodation_payment_way', 'accommodation_payment_description', 
        'participation_local_cost', 'participation_local_currency', '', 'participation_payment_way', 'participation_payment_description',
        'additional_expenses_initial', 'additional_expenses_initial_description', 'user_recommendation', 'secretary_recommendation']
      },
      {
        'label': 'secretary_data.label',
        'fields': ['movement_id', 'trip_days_before', 'expenditure_date_protocol',
        'expenditure_protocol', 'movement_date_protocol', 'movement_protocol',]
      },
      {
        'label': 'computed_data.label',
        'fields': ['transport_days_manual', 'transport_days_proposed', 'overnights_num_manual', 'overnights_proposed', 
        'compensation_days_manual', 'compensation_days_proposed', 'trip_days_before', 'trip_days_after', 
        'overnights_sum_cost', 'same_day_return_task', 'compensation_final', 'compensation_level', 'total_cost',]
      },
    ],
    layout: {
      flex: [
        50, 50, 50, 50, 50, 100, 50, 50, 50, 50,   //10
        50, 50, 50, 50, 50, 50, 50, 50, 50, 50,    //20
        50, 50, 50, 50, 50, 50, 50, 50, 50, 50,    //30
        50, 50, 33, 50, 50, 50, 50, 50, 50, 50,    //40
        50, 50, 50, 50, 100, 50, 50, 50, 50, 50,   //50
        50, 50, 30, 20, 50, 100, 100, 50, 50, 50,  //60
        50, 50, 50, 50, 50, 30, 20,                //70
      ] 
    }
  }
};

