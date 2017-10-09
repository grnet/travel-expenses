export const UIS = {
  "petition_user": {
    fieldsets: [
      {
        'label': 'user_data.label',
        'fields': ['first_name', 'last_name', 'specialty', 'kind', 'tax_reg_num', 'tax_office', 'iban', 'user_category']
      },
      {
        'label': 'travel_data.label',
        'fields': [['dse',{attrs:{disabled: true}}], 'project', 'reason',
        'task_start_date', 'task_end_date', 'participation_local_cost', 'participation_local_currency', 'user_recommendation']
      },
      {
        'label': 'travel_data.label',
        'fields': ['travel_info'],
      },
    ],
    layout: {
      flex: [
      50, 50, 50, 50, 50, 50, 50, 50, 50, 50,     //10
      50, 100, 50, 50, 50, 50, 50, 50, 50, 50,    //20
      50, 50, 100, 100, 100, 50, 50, 50, 50, 50,  //30
      50, 50, 30, 20
      ]
    }
  },
  "petition_travel": {
    layoutMap: {"reason": 100},
    fieldsets: [
      {
        'label': 'manager_approval.label',
        'fields': [['manager_movement_approval',{attrs:{disabled: true}}], ['manager_cost_approval',{attrs:{disabled: true}}],]
      },
      {
        'label': 'user_data.label',
        'fields': ['first_name', 'last_name', 'specialty', 'kind', 'tax_reg_num', 'tax_office', 'iban', 'user_category']
      },
      {
        'label': 'travel_data.label',
        'fields': [['dse',{attrs:{disabled: false}}], 'project', 'reason',
        'task_start_date', 'task_end_date', 'participation_cost', 'participation_local_cost', 'participation_local_currency', 'participation_payment_way', 
        'participation_payment_description', 'additional_expenses_initial', 'additional_expenses_initial_description', 'non_grnet_quota', 
        ['user_recommendation',{attrs:{readonly: true}}], 'secretary_recommendation']
      },
      {
        'label': 'travel_data.label',
        'fields': ['travel_info'],
      },
      {
        'label': 'secretary_data.label',
        'fields': ['movement_id', 'trip_days_before', 'expenditure_date_protocol',
        'expenditure_protocol', 'movement_date_protocol', 'movement_protocol',]
      },
      {
        'label': 'computed_data.label',
        'fields': ['trip_days_before', ['trip_days_after',{attrs:{disabled: true}}], 
        'same_day_return_task', 'overnights_sum_cost', 'compensation_final', 'total_cost']
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
        100, 50, 50, 50, 50, 100, 50, 50, 40, 10     //70

      ]
    }
  },
  "compensation_user": {
    fieldsets: [
      {
        'label': 'travel_data.label',
        'fields': [['dse', {attrs:{disabled: true}}], ['project', {attrs:{disabled: true}}], ['reason', {attrs:{disabled: true}}],
        ['task_start_date', {attrs:{disabled: true}}], ['task_end_date', {attrs:{disabled: true}}]]
      },
      {
        'label': 'travel_data.label',
        'fields': ['travel_info'],
      },
      {
        'label': 'travel_report.label',
        'fields': ['travel_files', 'additional_expenses', 'additional_expenses_local_currency', 'additional_expenses_description']
      },
    ],
    layout: {
      flex: [
        50, 50, 100, 100, 100, 50, 100, 100, 50, 50, //10
        50, 50, 100, 100, 50, 50, 50, 50, 50, 50,    //20
        50, 50, 50, 50, 50, 50, 50, 50, 50, 50,      //30
        50, 50, 50, 50, 50, 50, 50, 50, 50, 50,      //40
        50, 50, 50, 50, 50, 50, 50, 50, 50, 50,      //50
        50, 50, 100, 50, 50, 50, 50, 50, 50, 50,     //60
        40, 10, 50, 50, 100, 100, 50, 50, 50, 50,    //70
        50, 50, 50, 40, 10,                          //80
      ]
    }
  },
  "compensation_secretary": {
    fieldsets: [
      {
        'label': 'timesheets.label',
        'fields': ['timesheeted']
      },
      {
        'label': 'travel_report.label',
        'fields': [['travel_files', {attrs:{disabled: true}}],
        ['additional_expenses', {label:'additional_expenses_user.label'}], 
        'additional_expenses_local_currency', 
        ['additional_expenses_description', {label:'additional_expenses_description_user.label'}]]
      },
      {
        'label': 'manager_approval.label',
        'fields': [['manager_movement_approval', {attrs:{disabled: true}}], ['manager_cost_approval', {attrs:{disabled: true}}],]
      },
      {
        'label': 'user_data.label',
        'fields': ['first_name', 'last_name', 'specialty', 'kind', 'tax_reg_num', 'tax_office', 'iban', 'user_category']
      },
      {
        'label': 'travel_data.label',
        'fields': [['dse', {attrs:{disabled: true}}], ['project', {attrs:{disabled: true}}], ['reason', {attrs:{disabled: true}}],
        ['task_start_date', {attrs:{disabled: true}}], ['task_end_date', {attrs:{disabled: true}}],
        'participation_cost', 'participation_local_cost', 'participation_local_currency', 'participation_payment_way', 'participation_payment_description', 
        ['additional_expenses_initial', {attrs:{disabled: true}}], ['additional_expenses_initial_description', {attrs:{disabled: true}}], 
        'non_grnet_quota', ]
      },
      {
        'label': 'travel_data.label',
        'fields': ['travel_info'],
      },
      {
        'label': 'controller_data.label',
        'fields': [['movement_id', {attrs:{disabled: true}}], ['trip_days_before', {attrs:{disabled: true}}],
        ['expenditure_date_protocol', {attrs:{disabled: true}}], ['expenditure_protocol', {attrs:{disabled: true}}],
        ['movement_date_protocol', {attrs:{disabled: true}}], ['movement_protocol', {attrs:{disabled: true}}],
        'compensation_petition_date', 'compensation_petition_protocol', 'compensation_decision_date', 'compensation_decision_protocol']
      },
      {
        'label': 'computed_data.label',
        'fields': [['trip_days_before', {attrs:{disabled: true}}], ['trip_days_after',{attrs:{disabled: true}}],
        ['same_day_return_task', {attrs:{disabled: true}}], ['overnights_sum_cost', {attrs:{disabled: true}}],
        ['compensation_final', {attrs:{disabled: true}}], ['total_cost', {attrs:{disabled: true}}]]
      },
    ],
    layout: {
      flex: [
        50, 50, 50, 50, 50, 50, 50, 100, 100, 100,   //10
        50, 100, 100, 50, 50, 50, 50, 100, 100, 50,  //20
        50, 50, 50, 50, 50, 50, 100, 50, 50, 50,     //30
        50, 50, 50, 50, 50, 50, 50, 50, 50, 50,      //40
        50, 50, 50, 50, 50, 50, 50, 50, 50, 50,      //50
        50, 50, 50, 50, 50, 50, 50, 100, 50, 50,     //60
        50, 50, 50, 50, 50, 40, 10, 50, 50, 100,     //70
        100, 50, 50, 50, 50, 50, 50, 50, 40, 10,     //80
      ]
    }
  },

  //view mode templates
  "petition_travel_view": {
  layoutMap: {"reason": 100},
  fieldsets: [
    {
      'label': 'manager_approval.label',
      'fields': [['manager_movement_approval', {attrs:{disabled: true}}], ['manager_cost_approval', {attrs:{disabled: true}}],]
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
      ['accommodation_local_cost', {attrs:{disabled: true, label:'accommodation_local_cost_user.label'}}], 
      ['accommodation_local_currency', {attrs:{disabled: true}}], 
      ['accommodation_payment_way', {attrs:{disabled: true}}], ['accommodation_payment_description', {attrs:{disabled: true}}], 
      ['participation_cost', {attrs:{disabled: true}}],
      ['participation_local_cost', {attrs:{disabled: true, label:'participation_local_cost_user.label'}}], 
      ['participation_local_currency', {attrs:{disabled: true}}], 
      ['participation_payment_way', {attrs:{disabled: true}}], ['participation_payment_description', {attrs:{disabled: true}}], 
      ['additional_expenses_initial',{attrs:{disabled: true}}], 
      ['additional_expenses_initial_description', {attrs:{disabled: true}}], ['meals', {attrs:{disabled: true}}], 
      ['non_grnet_quota', {attrs:{disabled: true}}], 
      ['user_recommendation',{attrs:{disabled: true}}], ['secretary_recommendation', {attrs:{disabled: true}}]]
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
},

  "compensation_secretary_view": {
  layoutMap: {"reason": 100},
  fieldsets: [
    {
      'label': 'manager_approval.label',
      'fields': [['manager_movement_approval', {attrs:{disabled: true}}], ['manager_cost_approval', {attrs:{disabled: true}}],]
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
      ['accommodation_local_cost', {attrs:{disabled: true, label:'accommodation_local_cost_user.label'}}], 
      ['accommodation_local_currency', {attrs:{disabled: true}}], 
      ['accommodation_payment_way', {attrs:{disabled: true}}], ['accommodation_payment_description', {attrs:{disabled: true}}], 
      ['participation_cost', {attrs:{disabled: true}}],
      ['participation_local_cost', {attrs:{disabled: true, label:'participation_local_cost_user.label'}}], 
      ['participation_local_currency', {attrs:{disabled: true}}], 
      ['participation_payment_way', {attrs:{disabled: true}}], ['participation_payment_description', {attrs:{disabled: true}}], 
      ['additional_expenses_initial',{attrs:{disabled: true}}], 
      ['additional_expenses_initial_description', {attrs:{disabled: true}}], ['meals', {attrs:{disabled: true}}], 
      ['non_grnet_quota', {attrs:{disabled: true}}], 
      ['user_recommendation',{attrs:{disabled: true}}], ['secretary_recommendation', {attrs:{disabled: true}}]]
    },
    {
      'label': 'secretary_data.label',
      'fields': [['movement_id', {attrs:{disabled: true}}], ['trip_days_before', {attrs:{disabled: true}}], 
        ['expenditure_date_protocol', {attrs:{disabled: true}}], ['expenditure_protocol', {attrs:{disabled: true}}], 
        ['movement_date_protocol', {attrs:{disabled: true}}], ['movement_protocol', {attrs:{disabled: true}}],
        ['compensation_petition_date', {attrs:{disabled: true}}], ['compensation_petition_protocol', {attrs:{disabled: true}}], 
        ['compensation_decision_date', {attrs:{disabled: true}}], ['compensation_decision_protocol', {attrs:{disabled: true}}]]
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
},
};

