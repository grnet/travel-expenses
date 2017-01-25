import Ember from 'ember';

const {
  set,
  get,
  computed,
} = Ember;

export default Ember.Mixin.create({
  
  model: [],

  page: 0,
  pages: [],
  limit: 5,
  limitOptions: Ember.A([5,10,15]),

  paginatedModel: computed('model.[]', 'page', 'limit',
  function() {
    let model = get(this, 'model'); 
    let page = parseInt(get(this, 'page'));
    let limit = parseInt(get(this, 'limit'));
    let pages = get(this, 'pages');
    let arrayEnd = Math.floor(model.length/limit) + (model.length%limit);

    for (var i=0; i < arrayEnd; i ++){
      pages[i] = i;
    }
    return model.slice(page * limit, limit * (page + 1));
  }),

  actions: {
    incrementPage() {
      let model = get(this, 'model');
      let page = get(this, 'page');
      let limit = parseInt(get(this, 'limit'));
      let arrayEnd = Math.floor(model.length/limit) + (model.length%limit);
      if (page < arrayEnd -1) {
        let newPage = page + 1;
        set(this, 'page', newPage); // this will trigger paginatedModel change
      }
    },
    decrementPage() { 
      let page = get(this, 'page');
      if (page > 0) {
        let newPage = page - 1;
        set(this, 'page', newPage); // this will trigger paginatedModel change
      }
    }
  }
});
