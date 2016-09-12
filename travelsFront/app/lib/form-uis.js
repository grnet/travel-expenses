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
      flex: [
      50, 50, 50, 50, 50, 50, 50, 50, 50, 50,    //10
      50, 100, 50, 50, 50, 50, 50, 50, 50, 30,   //20
      20, 50, 100, 100, 50, 50, 50, 50, 50, 50,  //30
      50, 50, 30, 20
      ]
    }
  },
  "petition_travel": {
    layoutMap: {"reason": 100},
    fieldsets: [
      {
        'label': 'manager_approval.label',
        'fields': ['manager_travel_approval', 'manager_final_approval',]
      },
      {
        'label': 'user_data.label',
        'fields': ['first_name', 'last_name', 'specialty', 'kind', 'tax_reg_num', 'tax_office', 'iban', 'user_category']
      },
      {
        'label': 'travel_data.label',
        'fields': ['dse', 'project', 'reason', 'departure_point', 'arrival_point','movement_category', 'country_category',
        'task_start_date', 'task_end_date', 'depart_date', 'return_date', 'means_of_transport', 'transportation_cost',
        'transportation_payment_way', 'transportation_payment_description', 'accommodation_cost', 
        ['accommodation_local_cost', {label:'accommodation_local_cost_user.label', attrs:{readonly: true}}], 'accommodation_local_currency', 
        'accommodation_payment_way', 'accommodation_payment_description', 'participation_cost',
        ['participation_local_cost', {label:'participation_local_cost_user.label', attrs:{readonly: true}}], 'participation_local_currency', 
        'participation_payment_way', 'participation_payment_description', 'additional_expenses_initial', 
        'additional_expenses_initial_description', 'meals', 'non_grnet_quota', 
        ['user_recommendation',{attrs:{readonly: true}}], 'secretary_recommendation']
      },
      {
        'label': 'secretary_data.label',
        'fields': ['movement_id', 'trip_days_before', 'expenditure_date_protocol',
        'expenditure_protocol', 'movement_date_protocol', 'movement_protocol',]
      },
      {
        'label': 'computed_data.label',
        'fields': ['transport_days_manual', 'transport_days_proposed', 'overnights_num_manual', 'overnights_proposed', 
        'compensation_days_manual', 'compensation_days_proposed', 'trip_days_before', ['trip_days_after',{attrs:{disabled: true}}], 
        'same_day_return_task', 'overnights_sum_cost', 'compensation_final', 'compensation_level', 'total_cost']
      },
    ],
    layout: {
      flex: [
        100, 100, 100, 50, 50, 50, 50, 50, 100, 50,  //10
        50, 50, 50, 50, 50, 50, 100, 50, 50, 100,    //20
        100, 50, 50, 50, 50, 50, 50, 50, 50, 50,     //30
        50, 50, 50, 50, 100, 100, 50, 50, 50, 50,    //40
        50, 50, 50, 50, 50, 50, 50, 100, 50, 50,     //50 
        50, 50, 50, 50, 50, 40, 10, 50, 50, 100,     //60 
        50, 50, 50, 50, 50, 100, 100, 100, 40, 10    //70 
      ] 
    }
  },
  "compensation_user": {
    fieldsets: [
      {
        'label': 'travel_report.label',
        'fields': ['travel_files', 'travel_report', 'additional_expenses', 'additional_expenses_local_currency', 'additional_expenses__description']
      },
      {
        'label': 'manager_approval.label',
        'fields': [['manager_travel_approval', {attrs:{disabled: true}}], ['manager_final_approval', {attrs:{disabled: true}}],]
      },
      {
        'label': 'user_data.label',
        'fields': ['first_name', 'last_name', 'specialty', 'kind', 'tax_reg_num', 'tax_office', 'iban', 'user_category']
      },
      {
        'label': 'travel_data.label',
        'fields': [['dse', {attrs:{disabled: true}}], ['project', {attrs:{disabled: true}}], ['reason', {attrs:{disabled: true}}], 
        ['departure_point', {attrs:{disabled: true}}], ['arrival_point', {attrs:{disabled: true}}], 'movement_category', 'country_category',
        ['task_start_date', {attrs:{disabled: true}}], ['task_end_date', {attrs:{disabled: true}}], ['depart_date', {attrs:{disabled: true}}], 
        ['return_date', {attrs:{disabled: true}}], ['means_of_transport', {attrs:{disabled: true}}], ['transportation_cost', {attrs:{disabled: true}}],
        ['transportation_payment_way', {attrs:{disabled: true}}], ['transportation_payment_description', {attrs:{disabled: true}}], 
        ['accommodation_cost', {attrs:{disabled: true}}], 
        ['accommodation_local_cost', {label:'accommodation_local_cost_user.label', {attrs:{disabled: true}}}], 
        ['accommodation_local_currency', {attrs:{disabled: true}}], 
        ['accommodation_payment_way', {attrs:{disabled: true}}], ['accommodation_payment_description', {attrs:{disabled: true}}], 
        ['participation_cost', {attrs:{disabled: true}}],
        ['participation_local_cost', {label:'participation_local_cost_user.label', {attrs:{disabled: true}}}], 
        ['participation_local_currency', {attrs:{disabled: true}}], 
        ['participation_payment_way', {attrs:{disabled: true}}], ['participation_payment_description', {attrs:{disabled: true}}], 
        ['additional_expenses_initial',{attrs:{readonly: true}}], 
        ['additional_expenses_initial_description', {attrs:{disabled: true}}], ['meals', {attrs:{disabled: true}}], 
        ['non_grnet_quota', {attrs:{disabled: true}}], 
        ['user_recommendation',{attrs:{readonly: true}}], ['secretary_recommendation', {attrs:{disabled: true}}]]
      },
      {
        'label': 'secretary_data.label',
        'fields': [['movement_id', {attrs:{disabled: true}}], ['trip_days_before', {attrs:{disabled: true}}], 
        ['expenditure_date_protocol', {attrs:{disabled: true}}], ['expenditure_protocol', {attrs:{disabled: true}}], 
        ['movement_date_protocol', {attrs:{disabled: true}}], ['movement_protocol', {attrs:{disabled: true}}]]
      },
      {
        'label': 'computed_data.label',
        'fields': [['transport_days_manual', {attrs:{disabled: true}}], ['transport_days_proposed', {attrs:{disabled: true}}], 
        ['overnights_num_manual', {attrs:{disabled: true}}], ['overnights_proposed', {attrs:{disabled: true}}], 
        ['compensation_days_manual', {attrs:{disabled: true}}], ['compensation_days_proposed', {attrs:{disabled: true}}], 
        ['trip_days_before', {attrs:{disabled: true}}], ['trip_days_after',{attrs:{disabled: true}}], 
        ['same_day_return_task', {attrs:{disabled: true}}], ['overnights_sum_cost', {attrs:{disabled: true}}], 
        ['compensation_final', {attrs:{disabled: true}}], ['compensation_level', {attrs:{disabled: true}}], 
        ['total_cost', {attrs:{disabled: true}}]]
      },
    ],
    layout: {
      flex: [
        100, 100, 100, 50, 50, 50, 50, 50, 100, 50,  //10
        50, 50, 50, 50, 50, 50, 100, 50, 50, 100,    //20
        100, 50, 50, 50, 50, 50, 50, 50, 50, 50,     //30
        50, 50, 50, 50, 100, 100, 50, 50, 50, 50,    //40
        50, 50, 50, 50, 50, 50, 50, 100, 50, 50,     //50 
        50, 50, 50, 50, 50, 40, 10, 50, 50, 100,     //60 
        50, 50, 50, 50, 50, 100, 100, 100, 40, 10    //70 
      ] 
    }
  }
};

