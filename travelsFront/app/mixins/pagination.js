import Ember from 'ember';

const {
  set,
  get,
  computed,
} = Ember;

export default Ember.Mixin.create({
  
  model: [],
  page: 1,  
  limit: 5,
  limitOptions: Ember.A([5,10,15]),

  pages: computed('model.length', 'limit',
  function() {
    let pages = [];
    let limit = parseInt(get(this, 'limit'));    
    let modelSize = get(this, 'model.length');
    let arrayEnd = Math.floor(modelSize/limit) + (modelSize%limit);

    for (var i=1; i < arrayEnd + 1; i ++){
      pages[i] = i;
    }
    return pages;
  }),
  
  paginatedModel: computed('model.[]', 'page', 'limit',
  function() {
    let model = get(this, 'model'); 
    let page = parseInt(get(this, 'page'));
    let limit = parseInt(get(this, 'limit'));   
    return model.slice((page - 1) * limit, limit * page);
  }),

  actions: {
    incrementPage() {
      let model = get(this, 'model');
      let page = get(this, 'page');
      let limit = parseInt(get(this, 'limit'));
      let pagesLength = get(this, 'pages.length');;
      if (page < pagesLength-1) {
      	let newPage = page + 1;
      	set(this, 'page', newPage); // this will trigger paginatedModel change
    	}
    },
    decrementPage() { 
    	let page = get(this, 'page');
    	if (page > 1) {
	      let newPage = page - 1;
	      set(this, 'page', newPage); // this will trigger paginatedModel change
      }
    }
  }
});
