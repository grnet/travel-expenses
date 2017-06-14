import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'travels-front/config/environment'; 

const CHOICES = ENV.APP.resource_choices,
      CURRENCY = [[ENV.default_currency, ENV.default_currency]];

const {
  get,
  set
} = Ember;

export var Petition = DS.Model.extend({
  session: Ember.inject.service('session'),
  // profile fields
  first_name: DS.attr({attrs: {disabled: true, required: true}}),
  last_name: DS.attr({attrs: {disabled: true, required: true}}),
  specialty: DS.attr({'choices': CHOICES.SPECIALTY, attrs: {disabled: true}}),
  kind: DS.attr({'choices': CHOICES.KIND, attrs: {disabled: true}}),
  tax_reg_num: DS.attr({attrs: {disabled: true}}),
  tax_office: DS.belongsTo('tax-office', {attrs: {disabled: true}}),
  iban: DS.attr({attrs: {disabled: true, required: true}}),
  user_category: DS.attr({'choices': CHOICES.USER_CATEGORY, attrs: {disabled: true}}),
  //petition fields
  user: DS.attr('string'),
  dse: DS.attr('string', {attrs: {required: true}}),
  project: DS.belongsTo('project', {attrs: {required: true}, component: 'sort-model'}),
  reason: DS.attr({attrs: {required: true, textarea: true}}),
  movement_category: DS.attr({choices: CHOICES.MOVEMENT_CATEGORIES, attrs: {disabled: true}}),
  country_category: DS.attr('string', {attrs: {disabled: true}}),
  created: DS.attr('date', {attrs: {time: true, required: true}}),
  updated: DS.attr('date', {attrs: {time: true, required: true}}),
  task_start_date: DS.attr('date', {
    onChange(object, key, value) {
    if (!get(object, 'task_end_date')) { set(object, 'task_end_date', value);}
    },
    attrs: {
      time: true,
      required: true
    }}),
  task_end_date: DS.attr('date', {
    attrs: {
      time: true,
      required: true
    }}),
  status: DS.attr({'choices': CHOICES.STATUS, attrs: {disabled: true}}),
  petition_id: Ember.computed('id', function(){
    // return just the status id
    return _.last(this.get('id').replace(/\/$/, '').split('/'));
  }),
  participation_local_cost: DS.attr({attrs: {required: true}}),
  participation_local_currency: DS.attr({'choices': CURRENCY, 'component': 'petition-currency'}),
  additional_expenses_initial: DS.attr({attrs: {required: true}}),
  additional_expenses_initial_description: DS.attr({attrs:{textarea: true}}),
  user_recommendation: DS.attr({attrs:{textarea: true}}),

  //Travel_info DATA
  travel_info: DS.attr('array', {'component': 'travel-info'}),
  
  //set movement/country category value
  observeDeparturePoint: Ember.observer('arrival_point', function() {
    this.get('arrival_point').then((city) => {
      if (this.get('isDeleted')) { return; }
      if (!city) {
        this.set('country_category', null);
        this.set('movement_category', null);
      } else {
        this.set('country_category', city.get('country.category'));
        if (city.get('country.name') == 'Ελλάδα') {
          this.set('movement_category', '1');
        } else {
          this.set('movement_category', '2');
        }
      }
    })
  }),

  // set status label value
  status_label: Ember.computed('status', function(){
    var status =this.get('status');
    var label=CHOICES.STATUS[status-1];
    console.log("Status no. ", label[0]);
    return label[1] || status;
  }),

  needsApproval: Ember.computed('manager_movement_approval', function() {
    return this.get('manager_movement_approval');
  }),

  needsCostApproval: Ember.computed('manager_cost_approval', function() {
    return this.get('manager_cost_approval');
  }),

  
  // propagate travel_info errors to the related travel info local model fields
  observeTravelInfoErrors: Ember.observer('errors.travel_info', function() {
    let errors = this.get('errors.travel_info');
    if (!errors) { return; }
    errors.forEach((err) => {
      Object.keys(err.message).forEach((key) => {
        let msgs = err.message[key];
        this.set('errors.' + key, Ember.A([Ember.Object.create({
          attribute: key,
          message: msgs[0]
        })]));
      });
    })
  }),

  cloneAs(modelName) {
    let clone = this.store.createRecord(modelName);
    let type = clone.constructor;
    type.eachAttribute((name) => {
      clone.set(name, this.get(name));
    });
    type.eachRelationship((name) => {
      clone.set(name, this.get(name));
    });
    return clone;
  },

  compensationSubmit: function(){
    let adapter = this.store.adapterFor(this.constructor.modelName);
    let model = this;
    return adapter.action(this, 'submit').then(function() {
      return model;
    }).catch((apiError) => { 
        let modelErrors = model.get('errors') // ta error data tou model
        apiError.errors.forEach((err) => {
        let attr = err.source.pointer.split('/').slice(-1)[0];
        let msg = err.detail;
        modelErrors.set(attr, [msg]);

        throw apiError;
      });
    });
  },

  pdfExport: function(petition, pdf_id){
    var token = this.get("session.data.authenticated.auth_token");
    var base_url = this.store.adapterFor(petition.constructor.modelName).urlForModel(petition);
    var extension_url = '';
    var pdf_name = '';
    var dse = petition.get('dse');

    switch(pdf_id){
      case "1":
      case "3":
        extension_url = 'application_report/';
        pdf_name = 'application';
        break;
      case "2":
      case "4":
        extension_url = 'decision_report/';
        pdf_name = 'decision';
        break;
    };

    return $.ajax({
      headers:{
        Authorization: 'Token ' + token
      },
      xhrFields : {
        responseType : 'arraybuffer'
      },
      url: base_url + extension_url,
      success: function(data) {
          var blob=new Blob([data], { type: "application/pdf" });
          var link=document.createElement('a');
          link.href=window.URL.createObjectURL(blob);
          link.download=pdf_name+"_dse["+dse+"]"+".pdf";
          link.click();
      }
    });
 },

 approve: function(){
    let adapter = this.store.adapterFor(this.constructor.modelName);
    let model = this;
    return adapter.action(this, 'president_approval').then(function() {
      model.unloadRecord();
      return model;
    });
  },

  cancel: function() {
    let adapter = this.store.adapterFor(this.constructor.modelName);
    let model = this;
    return adapter.action(this, 'cancel').then(function() {
      model.unloadRecord();
      return model;
    });
  }
});
