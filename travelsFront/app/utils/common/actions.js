import Ember from 'ember';
import fetch from "ember-network/fetch";

const {
  computed,
  get,
} = Ember;

/*We compute the value of the hidden property in accordance with the role of the user
and the status of the application. We have also mapped the status number with the position
in the array showButtonBy. We have set the value of each of the array's elements,
depending on whether the respective button should be shown or not*/

const submit = {
  label: 'prompt_submit_title',
  icon: 'assignment_returned',
  accent: true,
  hidden: computed('model.status', 'role',  function(){
    let status = this.get('model.status');
    let role = this.get('role');
    if (role === 'USER' || role === 'MANAGER') {
      let showButtonBy = [false, true, true, true, true, false, true, true, true, true];
      return showButtonBy[status-1];
    }
  }),
  action: function(route, model) {
    let messages = route.get('messageService');
    let token = get(route, 'user.auth_token');
    let store = get(route, 'store');
    let adapter = store.adapterFor('application-item');
    let url = adapter.buildURL('application-item', get(model, 'id'), 'findRecord');
    return fetch(url + 'submit/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Token ${token}`
      },
    }).then((resp) => {
      if (resp.status === 200) {
        model.reload().then(() => {
          messages.setSuccess('submit.application.success');
        });
      } else {
        throw new Error('error');
      }
    }).catch((err) => {
      messages.setError('submit.application.error');
    });
  },

  confirm: true,
  prompt: {
    ok: 'form.button.submit',
    cancel: 'form.button.cancel',
    message: 'prompt_submit_message',
    title: 'prompt_submit_title',
  }
};

const undo = {
  label: 'prompt_undo_title',
  icon: 'undo',
  accent: true,
  hidden: computed('model.status', 'role', function(){
    let status = this.get('model.status');
    let role = this.get('role');
    if (role === 'USER' || role === 'MANAGER') {
      let showButtonBy = [true, false, true, true, true, true, false, true, true, true];
      return showButtonBy[status-1];
    }
  }),
  action: function(route, model) {
    let messages = route.get('messageService');
    let token = get(route, 'user.auth_token');
    let store = get(route, 'store');
    let adapter = store.adapterFor('application-item');
    let url = adapter.buildURL('application-item', get(model, 'id'), 'findRecord');
    return fetch(url + 'cancel/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Token ${token}`
      },
    }).then((resp) => {
      if (resp.status === 200) {
        model.reload().then(() => {
          messages.setSuccess('undo.application.success');
        });
      } else {
        throw new Error('error');
      }
    }).catch((err) => {
      messages.setError('undo.application.error');
    });
  },

  confirm: true,
  prompt: {
    ok: 'form.button.undo',
    cancel: 'form.button.cancel',
    message: 'prompt_undo_message',
    title: 'prompt_undo_title',
  }
};

let applicationActions = { submit: submit, undo: undo };

export { applicationActions };