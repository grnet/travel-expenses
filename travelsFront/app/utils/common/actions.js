import Ember from 'ember';
import fetch from 'ember-network/fetch';

const {
  computed,
  get,
} = Ember;

/* We compute the value of the hidden property in accordance with the role of the user
and the status of the application. We have also mapped the status number with the position
in the array showButtonBy. We have set the value of each of the array's elements,
depending on whether the respective button should be shown or not */

function action_utils(route, model) {
  let messages = route.get('messageService');
  let token = get(route, 'user.auth_token');
  let store = get(route, 'store');
  let adapter = store.adapterFor('application-item');
  let url = adapter.buildURL('application-item', get(model, 'id'), 'findRecord');

  return { messages, token, url };
};

function ajax_call(route, model, endpoint, msgSuccess, msgError) {
  let { messages, token, url } = action_utils(route, model);

  return fetch(url + endpoint + '/', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Authorization': `Token ${token}`,
    },
  }).then((resp) => {
    if (resp.status === 200) {
      route.refresh().then(() => {
        messages.setSuccess(msgSuccess);
      })
    } else {
      throw new Error('error');
    }
  }).catch((err) => {
    messages.setError(msgError);
  });
};

const submit = {
  label: 'prompt_submit_title',
  icon: 'send',
  classNames: 'md-success',
  action: function(route, model) {
    let endpoint = 'submit';
    let msgSuccess = 'submit.application.success';
    let msgError = 'submit.application.error';

    return ajax_call(route, model, endpoint, msgSuccess, msgError);
  },
  hidden: computed('model.status', 'role', function(){
    let status = this.get('model.status');
    let role = this.get('role');

    if (role === 'USER' || role === 'MANAGER') {
      let showButtonBy = [false, true, true, true, true, false, true, true, true, true];

      return showButtonBy[status - 1];
    } else if (role === 'SECRETARY') {
      let showButtonBy = [true, true, false, true, true, true, true, true, true, true];

      return showButtonBy[status - 1];
    } else if (role === 'CONTROLLER') {
      let showButtonBy = [true, true, true, true, true, true, true, false, true, true];

      return showButtonBy[status - 1];
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
  },
};

const undo = {
  label: 'prompt_undo_title',
  icon: 'reply',
  accent: true,
  action: function(route, model) {
    let endpoint = 'cancel';
    let msgSuccess = 'undo.application.success';
    let msgError = 'undo.application.error';

    return ajax_call(route, model, endpoint, msgSuccess, msgError);
  },
  hidden: computed('model.status', 'role', function(){
    let status = this.get('model.status');
    let role = this.get('role');

    if (role === 'USER' || role === 'MANAGER') {
      let showButtonBy = [true, false, true, true, true, true, false, true, true, true];

      return showButtonBy[status - 1];
    } else if (role === 'SECRETARY') {
      let showButtonBy = [true, true, true, false, false, true, true, true, true, true];

      return showButtonBy[status - 1];
    } else if (role === 'CONTROLLER') {
      let showButtonBy = [true, true, true, true, true, true, true, true, false, false];

      return showButtonBy[status - 1];
    } else {
      return true;
    }
  }),
  confirm: true,
  prompt: {
    ok: 'form.ok.label',
    cancel: 'form.cancel.label',
    message: 'prompt_undo_message',
    title: 'prompt_undo_title',
  },
};

const pdf = {
  label: 'prompt_pdf_title',
  icon: 'file_download',
  accent: true,
  classNames: 'md-action',
  action: function(route, model) {
    let { messages, token, url } = action_utils(route, model);
    var dse = model.get('dse');

    return $.ajax({
      headers:{
        Authorization: 'Token ' + token,
      },
      xhrFields : {
        responseType : 'arraybuffer',
      },
      url: url + 'application_report/',
      success: function(data) {
        var blob = new Blob([data], { type: 'application/pdf' });
        var link = document.createElement('a');

        link.href = window.URL.createObjectURL(blob);
        link.download = 'application_' + 'dse[' + dse + ']' + '.pdf';
        link.click();
      },
    }).then((resp) => {
      if (resp.byteLength > 0) {
        return $.ajax({
          headers:{
            Authorization: 'Token ' + token,
          },
          xhrFields : {
            responseType : 'arraybuffer',
          },
          url: url + 'decision_report/',
          success: function(data) {
            var blob = new Blob([data], { type: 'application/pdf' });
            var link = document.createElement('a');

            link.href = window.URL.createObjectURL(blob);
            link.download = 'decision_' + 'dse[' + dse + ']' + '.pdf';
            link.click();
          },
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

      return showButtonBy[status - 1];
    } else if (role === 'CONTROLLER') {
      let showButtonBy = [true, true, true, true, true, true, true, true, false, true];

      return showButtonBy[status - 1];
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
    let endpoint = 'president_approval';
    let msgSuccess = 'approve.application.success';
    let msgError = 'approve.application.error';

    return ajax_call(route, model, endpoint, msgSuccess, msgError);
  },
  hidden: computed('model.status', 'role', function(){
    let status = this.get('model.status');
    let role = this.get('role');

    if (role === 'SECRETARY') {
      let showButtonBy = [true, true, true, false, true, true, true, true, true, true];

      return showButtonBy[status - 1];
    } else if (role === 'CONTROLLER') {
      let showButtonBy = [true, true, true, true, true, true, true, true, false, true];

      return showButtonBy[status - 1];
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
  },
};

const addToTimesheets = {
  label: 'tooltip_addToTimesheets',
  icon: 'today',
  classNames: computed('model.timesheeted', function(){
    let timesheeted = this.get('model.timesheeted');

    if (timesheeted == true) {
      return 'md-addToTimesheets';
    } else if (timesheeted == false) {
      return 'md-neutral';
    }
  }),
  action: function(route, model) {
    let endpoint = 'update_timesheeted';
    let msgSuccess = 'add.to.timesheets.success';
    let msgError = 'add.to.timesheets.error';

    return ajax_call(route, model, endpoint, msgSuccess, msgError);
  },
  hidden: computed('model.status', 'role', function(){
    let status = this.get('model.status');
    let role = this.get('role');

    if (role === 'CONTROLLER') {
      let showButtonBy = [true, true, true, true, false, false, false, false, false, false];

      return showButtonBy[status - 1];
    } else {
      return true;
    }
  }),
};

const withdraw = {
  label: computed('model.withdrawn', function(){
    let withdrawn = this.get('model.withdrawn');

    if (withdrawn == true) {
      return 'tooltip_withdraw_cancel';
    } else if (withdrawn == false) {
      return 'tooltip_withdraw';
    }
  }),
  icon: computed('model.withdrawn', function(){
    let withdrawn = this.get('model.withdrawn');

    if (withdrawn == true) {
      return 'do_not_disturb_off';
    } else if (withdrawn == false) {
      return 'do_not_disturb_on';
    }
  }),
  classNames: computed('model.withdrawn', function(){
    let withdrawn = this.get('model.withdrawn');

    if (withdrawn == true) {
      return 'md-neutral';
    } else if (withdrawn == false) {
      return 'md-withdrawn';
    }
  }),
  action: function(route, model) {
    let withdrawn = model.get('withdrawn');
    let endpoint = '';
    let msgSuccess = '';
    let msgError = '';

    if (withdrawn == true) {
      endpoint = 'cancel_withdrawal';
      msgSuccess = 'cancel.withdraw.application.success';
      msgError = 'cancel.withdraw.application.error';
    } else if (withdrawn == false) {
      endpoint = 'withdraw';
      msgSuccess = 'withdraw.application.success';
      msgError = 'withdraw.application.error';
    }

    return ajax_call(route, model, endpoint, msgSuccess, msgError);
  },
  hidden: computed('model.status', 'role', function(){
    let status = this.get('model.status');
    let role = this.get('role');

    if (role === 'SECRETARY') {
      let showButtonBy = [true, true, false, true, true, true, true, true, true, true];

      return showButtonBy[status - 1];
    } else if (role === 'CONTROLLER') {
      let showButtonBy = [true, true, true, true, true, true, true, false, true, true];

      return showButtonBy[status - 1];
    } else {
      return true;
    }
  }),
  confirm: true,
  prompt: {
    ok: 'form.ok.label',
    cancel: 'form.cancel.label',
    message:  computed('model.withdrawn', function(){
      let withdrawn = this.get('model.withdrawn');

      if (withdrawn == true) {
        return 'prompt_withdrawCancel_message';
      } else if (withdrawn == false) {
        return 'prompt_withdraw_message';
      }
    }),
    title:  computed('model.withdrawn', function(){
      let withdrawn = this.get('model.withdrawn');

      if (withdrawn == true) {
        return 'prompt_withdrawCancel_title';
      } else if (withdrawn == false) {
        return 'prompt_withdraw_title';
      }
    }),
  },
};

const exportStats = {
  label: 'tooltip_stats_title',
  icon: 'file_download',
  action: function(route, model) {
    let messages = route.get('messageService');
    let token = get(route, 'user.auth_token');
    let store = get(route, 'store');
    let adapter = store.adapterFor('project');
    let url = adapter.buildURL('project');
    var filename = 'travel_statistics';

    return $.ajax({
      headers:{
        Authorization: 'Token ' + token,
      },
      xhrFields : {
        responseType : 'arraybuffer',
      },
      url: url + 'stats/?response_format=csv',
      success: function(data) {
        var blob = new Blob([data], { type: 'text/csv' });
        var link = document.createElement('a');

        link.href = window.URL.createObjectURL(blob);
        link.download = filename + '.csv';
        link.click();
      },
    }).then((resp) => {
      if (resp.byteLength > 0) {
        route.refresh().then(() => {
          messages.setSuccess('stats.export.success');
        })
      } else {
        throw new Error('error');
      }
    }).catch((err) => {
      messages.setError('stats.export.error');
    });
  },
  hidden: computed('role', function(){
    let role = this.get('role');

    if (role === 'CONTROLLER') {
      return false;
    } else {
      return true;
    }
  }),
  confirm: false,
};

const change_password = {
  raised: false,
  label: 'password.change',
  confirm: true,
  action: function() {},
  prompt: {
    title: 'password.change.title',
    contentComponent: 'change-password',
    noControls: true
  }
};

let applicationActions = {
  submit: submit,
  undo: undo,
  pdf: pdf,
  approve: approve,
  addToTimesheets: addToTimesheets,
  withdraw: withdraw,
  exportStats: exportStats,
  change_password: change_password,
};

export { applicationActions };
