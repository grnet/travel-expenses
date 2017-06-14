import Ember from 'ember';
import BaseField from './model-form/fields/base';

const {
  get,
  set,
  isArray,
  computed,
  computed: { alias, equal, gt } 
} = Ember;

const Travel = Ember.Object.extend({
	arrival_city: computed('arrival_point', function() {
		let point = get(this, 'arrival_point');
		if (!point) { return null }
		let id = 3; // TODO: extract id from point
		return this.get('store').peekRecord('city', id);
	})
});


export default Ember.Component.extend(BaseField, {
	
	allCities: computed(function() {
		return this.get('store').findAll('city');
	}),

	arrivalChoice: computed(function() {
		return {label: this.get('arrival_city.name'), value: this.get('arrival_city.id')}
	}),

	cityChoices:Ember.computed('allCities.[]', function() {
		let cities = this.get('allCities');
		return cities.map((city) => { 
			return { label: get(city, 'name'), value: get(city, 'id') }
		});
	}),
	

	onArrivalChoice: Ember.observer('arrivalChoice.value', function() {
		let city = this.get('arrivalChoice');
		debugger;
	}),

  cities: computed('value', function() {
    let value = get(this, 'value');

    if (!value) {
      return [] // an to value einai null h undefined epistrefoume keno array
    }

    let infos = value.map((info) => {
    	return Travel.extend({store: this.get('store')}).create(info);
    });
    console.log(infos);
    return infos;
  }),

	actions: {
		addPair() {
		  let value = Ember.this.get('cities').concat();
		  value.addObject({
		    departure: '',
		    arrival: ''
		  });
		  this.onChange(value);
		},
		removePair() {
		  let value = Ember.this.get('cities').concat();
		  value = value.slice(-1);
		  this.onChange(value);
		},

		onFieldChange(index, field, newval) {
			let value = this.get('cities').concat();
			let curr = value[index].get(field);
			if (curr != newval) {
		  	value[index].set(field, newval);
		  	//this.onChange(value)
			}

		}
	}

});
