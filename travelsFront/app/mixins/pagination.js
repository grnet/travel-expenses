import Ember from 'ember';

const {
  set,
  get,
  computed,
} = Ember;

export default Ember.Mixin.create({
  
  modelToPaginate: Ember.computed.reads('filteredModel'),
  page: 1,  
  limit: 10,
  limitOptions: Ember.A([5,10,15]),

  pages: computed('modelToPaginate.length', 'limit', function() {
    let pages = []; 
    let limit = parseInt(get(this, 'limit'));    
    let modelSize = get(this, 'modelToPaginate.length');
    var arrayEnd = 0;

    if (modelSize%limit == 0) {
      arrayEnd = Math.floor(modelSize/limit);
    } else {
      arrayEnd = Math.floor(modelSize/limit) + 1;
    };
    
    for (var i=1; i < arrayEnd + 1; i ++){
      pages[i] = i;
    }
    return pages;
  }),
  
  paginatedModel: computed('modelToPaginate.[]', 'page', 'limit', function() {
    let model = get(this, 'modelToPaginate');
    let page = parseInt(get(this, 'page'));
    let limit = parseInt(get(this, 'limit'));   
    return model.slice((page - 1) * limit, limit * page);
  }),

  actions: {
    incrementPage() {
      let model = get(this, 'modelToPaginate');
      let page = get(this, 'page');
      let limit = parseInt(get(this, 'limit'));
      let pagesLength = get(this, 'pages.length');
      if (page < pagesLength-1) {
      	let newPage = page + 1;
      	set(this, 'page', newPage); // this will trigger modelToPaginate change
    	}
    },
    decrementPage() { 
    	let page = get(this, 'page');
    	if (page > 1) {
	      let newPage = page - 1;
	      set(this, 'page', newPage); // this will trigger modelToPaginate change
      }
    }
  }
});
