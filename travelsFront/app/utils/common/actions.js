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

function action_utils(route, model) {
  let messages = route.get('messageService');
  let token = get(route, 'user.auth_token');
  let store = get(route, 'store');
  let adapter = store.adapterFor('application-item');
  let url = adapter.buildURL('application-item', get(model, 'id'), 'findRecord');
  return {messages, token, url};
};

const submit = {
  label: 'prompt_submit_title',
  icon: 'flight',
  classNames: 'md-success',
  action: function(route, model) {
    let messages = action_utils(route, model).messages;
    let token = action_utils(route, model).token;
    let url = action_utils(route, model).url;
    return fetch(url + 'submit/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Token ${token}`
      },
    }).then((resp) => {
      if (resp.status === 200) {
        route.refresh().then(() => {
          messages.setSuccess('submit.application.success');
        })
      } else {
        throw new Error('error');
      }
    }).catch((err) => {
      messages.setError('submit.application.error');
    });
  },
  hidden: computed('model.status', 'role', function(){
    let status = this.get('model.status');
    let role = this.get('role');
    if (role === 'USER' || role === 'MANAGER') {
      let showButtonBy = [false, true, true, true, true, false, true, true, true, true];
      return showButtonBy[status-1];
    } else if (role === 'SECRETARY') {
      let showButtonBy = [true, true, false, true, true, true, true, true, true, true];
      return showButtonBy[status-1];
    } else {
      return true;
    }
  }),
  confirm: true,
  prompt: {
    ok: 'form.submit.label',
    cancel: 'form.cancel.label',
    message: 'prompt_submit_message',
    title: 'prompt_submit_title',
  }
};

const undo = {
  label: 'prompt_undo_title',
  icon: 'reply',
  accent: true,
  action: function(route, model) {
    let messages = action_utils(route, model).messages;
    let token = action_utils(route, model).token;
    let url = action_utils(route, model).url;
    return fetch(url + 'cancel/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Token ${token}`
      },
    }).then((resp) => {
      if (resp.status === 200) {
        route.refresh().then(() => {
          messages.setSuccess('undo.application.success');
        })
      } else {
        throw new Error('error');
      }
    }).catch((err) => {
      messages.setError('undo.application.error');
    });
  },
  hidden: computed('model.status', 'role', function(){
    let status = this.get('model.status');
    let role = this.get('role');
    if (role === 'USER' || role === 'MANAGER') {
      let showButtonBy = [true, false, true, true, true, true, false, true, true, true];
      return showButtonBy[status-1];
    } else if (role === 'SECRETARY') {
      let showButtonBy = [true, true, true, false, false, true, true, true, true, true];
      return showButtonBy[status-1];
    } else {
      return true;
    }
  }),
  confirm: true,
  prompt: {
    ok: 'form.undo.label',
    cancel: 'form.cancel.label',
    message: 'prompt_undo_message',
    title: 'prompt_undo_title',
  }
};

const pdf = {
  label: 'prompt_pdf_title',
  icon: 'file_download',
  accent: true,
  classNames: 'md-action',
  action: function(route, model) {
    let messages = action_utils(route, model).messages;
    let token = action_utils(route, model).token;
    let url = action_utils(route, model).url;
    var dse = model.get('dse');
    return $.ajax({
      headers:{
        Authorization: 'Token ' + token
      },
      xhrFields : {
        responseType : 'arraybuffer'
      },
      url: url + 'application_report/',
      success: function(data) {
          var blob=new Blob([data], { type: "application/pdf" });
          var link=document.createElement('a');
          link.href=window.URL.createObjectURL(blob);
          link.download="application_"+"dse["+dse+"]"+".pdf";
          link.click();
      }
    }).then((resp) => {
      if (resp.byteLength > 0) {
        return $.ajax({
          headers:{
            Authorization: 'Token ' + token
          },
          xhrFields : {
            responseType : 'arraybuffer'
          },
          url: url + 'decision_report/',
          success: function(data) {
              var blob=new Blob([data], { type: "application/pdf" });
              var link=document.createElement('a');
              link.href=window.URL.createObjectURL(blob);
              link.download="decision_"+"dse["+dse+"]"+".pdf";
              link.click();
          }
        }).then((resp) => {
          if (resp.byteLength > 0) {
            route.refresh().then(() => {
              messages.setSuccess('pdf.application.success');
          })
          } else {
            throw new Error('error');
          }
        }).catch((err) => {
           messages.setError('pdf.decision.error');
        })
      } else {
        throw new Error('error');
      }
    }).catch((err) => {
      messages.setError('pdf.application.error');
    });
  },
  hidden: computed('model.status', 'role', function(){
    let status = this.get('model.status');
    let role = this.get('role');
    if (role === 'SECRETARY') {
      let showButtonBy = [true, true, true, false, true, true, true, true, true, true];
      return showButtonBy[status-1];
    } else {
      return true;
    }
  }),
  confirm: false,
};

const approve = {
  label: 'prompt_approve_title',
  icon: 'verified_user',
  classNames: 'md-approve',
  action: function(route, model) {
    let messages = action_utils(route, model).messages;
    let token = action_utils(route, model).token;
    let url = action_utils(route, model).url;
    return fetch(url + 'president_approval/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Token ${token}`
      },
    }).then((resp) => {
      if (resp.status === 200) {
        route.refresh().then(() => {
          messages.setSuccess('approve.application.success');
        })
      } else {
        throw new Error('error');
      }
    }).catch((err) => {
      messages.setError('approve.application.error');
    });
  },
  hidden: computed('model.status', 'role', function(){
    let status = this.get('model.status');
    let role = this.get('role');
    if (role === 'SECRETARY') {
      let showButtonBy = [true, true, true, false, true, true, true, true, true, true];
      return showButtonBy[status-1];
    } else {
      return true;
    }
  }),
  confirm: true,
  prompt: {
    ok: 'form.approve.label',
    cancel: 'form.cancel.label',
    message: 'prompt_approve_message',
    title: 'prompt_approve_title',
  }
};

let applicationActions = { submit: submit, undo: undo, pdf: pdf, approve: approve };

export { applicationActions };
