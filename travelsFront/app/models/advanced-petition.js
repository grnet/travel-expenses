import Ember from 'ember';
import DS from 'ember-data';
import {validator, buildValidations} from 'ember-cp-validations';

var Validations=buildValidations({

	taxRegNum: validator('afm-validator'),
	iban: validator('iban-validator'),
	project: [
		validator('presence', true),
	]


});

export default DS.Model.extend(Validations,{
	petition: DS.belongsTo('petition'),
	movement_num: DS.attr(),
	dse: DS.attr(),
	accomondation: DS.belongsTo('accomondation'),
	flight: DS.belongsTo('flight'),
	feeding: DS.belongsTo('feeding'),
	non_grnet_quota: DS.attr(),
	grnet_quota: DS.attr(),
	compensation: DS.belongsTo('compensation'),
	expenditure_protocol: DS.attr(), 
    expenditure_date_protocol: DS.attr(),
    movement_protocol: DS.attr(),
    movement_date_protocol: DS.attr(),
    compensation_petition_protocol: DS.attr(),
    compensation_petition_date: DS.attr(),
    compensation_decision_protocol: DS.attr(),
    compensation_decision_date: DS.attr(),
    transport_days_manual: DS.attr(),
    overnights_num_manual: DS.attr(),
    compensation_days_manual: DS.attr()
});
