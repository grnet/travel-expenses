import DS from 'ember-data';
import Ember from 'ember';
import ENV from 'travel/config/environment';
import { computeDateFormat } from '../lib/common';
import { computeDateTimeFormat } from '../lib/common';

const CHOICES = ENV.APP.resources;
const BROWSER_TZ = moment.tz.guess();

function findCityTZ(city, serializer) {
  const cityID = city.split('/').slice(-2)[0];
  if (!serializer.store.peekRecord('city', cityID)) {
    return;
  }
  const cityName = serializer.store.peekRecord('city', cityID);
  const cityTZ = cityName.data.timezone;
  return cityTZ;
};

function dateToUTC(date, timezone) {
  //Undo the transformation in UTC made by the browser based on its local time
  const dateInForm = moment.tz(date, BROWSER_TZ).format().slice(0, -6);
  //Transform the date in the correct timezone based on the arrival point
  const dateInCityTZ = moment.tz(dateInForm, timezone).format();
  //Transform date in UTC to send it to the server
  const dateInUTC = moment.utc(dateInCityTZ).format();

  return dateInUTC;
};

function dateToLocal(date, timezone) {
  //Transform the date in the correct timezone based on the arrival point
  const dateInCityTZ = moment.tz(date, timezone);
  //Transform the date to the browser's local timezone
  let dateFormat = '';
  if (dateInCityTZ._offset == -0) {
    dateFormat = moment(dateInCityTZ).format().slice(0, -1);
  } else {
    dateFormat = moment(dateInCityTZ).format().slice(0, -6);
  }
  const dateInUI = moment(moment(dateFormat).toDate()).format();

  return dateInUI;
};

export default DS.Model.extend({
  __api__: {
    path: 'applications',

    serialize(hash, snapshot, serializer) {
      if (hash['travel_files'] === '') {
        return hash;
      }
      const arrivalPointFirstTZ = findCityTZ(hash.travel_info[0].arrival_point, serializer);
      const arrivalPointLastTZ = findCityTZ(hash.travel_info[hash.travel_info.length - 1].arrival_point, serializer);
      const taskStartDate = hash.task_start_date;
      const taskEndDate = hash.task_end_date;
      const travelInfo = hash.travel_info;

      let travellingDatesFixed = travelInfo.map((travelInfo, i) => {
        if (travelInfo.depart_date) {
          const departurePointTZ = findCityTZ(travelInfo.departure_point, serializer);
          hash.travel_info[i]['depart_date'] = dateToUTC(travelInfo.depart_date, departurePointTZ);
        }
        if (travelInfo.return_date) {
          const arrivalPointTZ = findCityTZ(travelInfo.arrival_point, serializer);
          hash.travel_info[i]['return_date'] = dateToUTC(travelInfo.return_date, arrivalPointTZ);
        }
      });

      delete hash['travel_files'];
      hash['task_start_date'] = dateToUTC(taskStartDate, arrivalPointFirstTZ);
      hash['task_end_date'] = dateToUTC(taskEndDate, arrivalPointLastTZ);
      return hash;
    },

    normalize(hash, serializer) {
      const arrivalPointFirstTZ = findCityTZ(hash.travel_info[0].arrival_point, serializer);
      const arrivalPointLastTZ = findCityTZ(hash.travel_info[hash.travel_info.length - 1].arrival_point, serializer);
      const taskStartDate = hash.task_start_date + 'Z';
      const taskEndDate = hash.task_end_date + 'Z';
      const travelInfo = hash.travel_info;

      let travellingDatesFixed = travelInfo.map((travelInfo, i) => {
        if (travelInfo.depart_date) {
          const departDate = travelInfo.depart_date + 'Z';
          const departurePointTZ = findCityTZ(travelInfo.departure_point, serializer);
          hash.travel_info[i]['depart_date'] = dateToLocal(departDate, departurePointTZ);
        }

        if (travelInfo.return_date) {
          const returnDate = travelInfo.return_date + 'Z';
          const arrivalPointTZ = findCityTZ(travelInfo.arrival_point, serializer);
          hash.travel_info[i]['return_date'] = dateToLocal(returnDate, arrivalPointTZ);
        }
      });
      hash['task_start_date'] = dateToLocal(taskStartDate, arrivalPointFirstTZ);
      hash['task_end_date'] = dateToLocal(taskEndDate, arrivalPointLastTZ);
      return hash;
    }
  },

  session: Ember.inject.service('session'),
  // profile fields
  user_id: DS.attr(),
  first_name: DS.attr(),
  last_name: DS.attr(),
  specialty: DS.attr({ 'choices': CHOICES.SPECIALTY }),
  kind: DS.attr({ 'choices': CHOICES.KIND }),
  tax_reg_num: DS.attr(),
  tax_office: DS.belongsTo('tax-office', { formAttrs: { optionLabelAttr: 'full_label' } }),
  iban: DS.attr(),
  user_category: DS.attr({ 'choices': CHOICES.USER_CATEGORY, disabled: true }),
  // application - user fields
  user: DS.attr('string'),
  dse: DS.attr({ disabled: true }),
  project: DS.belongsTo('project', { autocomplete: true, formAttrs: { optionLabelAttr: 'name' } }),
  reason: DS.attr({ type: 'text' }),
  participation_local_cost: DS.attr(),
  participation_local_currency: DS.attr({ 'choices': CHOICES.CURRENCIES, autocomplete: true }),
  task_start_date: DS.attr('date', {
    formAttrs: {
      time: true,
      format: 'dd mmmm yyyy',
    },
  }),
  task_end_date: DS.attr('date', {
    formAttrs: {
      time: true,
      format: 'dd mmmm yyyy',
    },
  }),
  task_start_date_format: computeDateFormat('task_start_date'),
  task_end_date_format: computeDateFormat('task_end_date'),
  task_start_date_time_format: computeDateTimeFormat('task_start_date'),
  task_end_date_time_format: computeDateTimeFormat('task_end_date'),
  user_recommendation: DS.attr({ type: 'text' }),
  status: DS.attr({ type: 'select', 'choices': CHOICES.STATUS }),
  travel_info: DS.hasMany('travel-info', { displayComponent: 'display-travel-info' }),
  // application - secretary fields
  additional_expenses_initial: DS.attr(),
  additional_expenses_initial_description: DS.attr(),
  expenditure_date_protocol: DS.attr('date'),
  expenditure_date_protocol_format: computeDateFormat('expenditure_date_protocol'),
  expenditure_protocol: DS.attr(),
  movement_date_protocol: DS.attr('date'),
  movement_date_protocol_format: computeDateFormat('movement_date_protocol'),
  movement_protocol: DS.attr(),
  non_grnet_quota: DS.attr(),
  manager_movement_approval: DS.attr('boolean', { disabled: true,  displayComponent: 'display-boolean'}),
  participation_cost: DS.attr(),
  participation_payment_way: DS.attr({ 'choices': CHOICES.WAYS_OF_PAYMENT }),
  trip_days_before: DS.attr({ disabled: true }),
  trip_days_after: DS.attr({ disabled: true }),
  overnights_sum_cost: DS.attr({ disabled: true }),
  compensation_cost: DS.attr({ disabled: true }),
  total_cost_calculated: DS.attr({ disabled: true }),
  withdrawn: DS.attr('boolean', { disabled: true, displayComponent: 'display-boolean' }),
  // compensation - user fields
  additional_expenses: DS.attr(),
  additional_expenses_local_currency: DS.attr({ 'choices': CHOICES.CURRENCIES, autocomplete: true }),
  additional_expenses_description: DS.attr({ type: 'text' }),
  travel_files: DS.attr(),
  // compensation - controller fields
  compensation_petition_date: DS.attr('date'),
  compensation_petition_date_format: computeDateFormat('compensation_petition_date'),
  compensation_petition_protocol: DS.attr(),
  compensation_decision_date: DS.attr('date'),
  compensation_decision_date_format: computeDateFormat('compensation_decision_date'),
  compensation_decision_protocol: DS.attr(),
  compensation_final: DS.attr(),
  timesheeted: DS.attr('boolean'),
  new_id: DS.attr(),
  additional_expenses_grnet: DS.attr(),

  // set status label value
  status_label: Ember.computed('status', function() {
    var status = this.get('status');
    var label = CHOICES.STATUS[status - 1];

    return label[1] || status;
  }),

  specialty_label: Ember.computed('specialty', function() {
    let specialty = this.get('specialty');

    for (let pair of CHOICES.SPECIALTY) {
      if (pair[0] === specialty) {
        return pair[1] || specialty;
      }
    }
  }),

  kind_label: Ember.computed('kind', function() {
    let kind = this.get('kind');

    for (let pair of CHOICES.KIND) {
      if (pair[0] === kind) {
        return pair[1] || kind;
      }
    }
  }),

  participation_payment_way_label: Ember.computed('participation_payment_way', function() {
    let participation_payment_way = this.get('participation_payment_way');

    for (let pair of CHOICES.WAYS_OF_PAYMENT) {
      if (pair[0] === participation_payment_way) {
        return pair[1] || participation_payment_way;
      }
    }
  }),
});
