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
  let modelName = model.get('constructor.modelName');
  let adapter = store.adapterFor('application-item');
  let url = adapter.buildURL(modelName, get(model, 'id'), 'findRecord');

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
        if (endpoint === 'submit') {
          messages.setSuccess(msgSuccess);
          route.transitionTo('application-item.index');
        } else {
          route.refresh().then(() => {
            messages.setSuccess(msgSuccess);
          })
        }
    } else {
      throw new Error('error');
    }
  }).catch((err) => {
    messages.setError(msgError);
  });
};

const submit = {
  label: 'submit.label',
  icon: 'send',
  classNames: 'md-success',
  action: function(route, model) {
    let endpoint = 'submit';
    let msgSuccess = 'submit.application.success';
    let msgError = 'submit.application.error';

    return ajax_call(route, model, endpoint, msgSuccess, msgError);
  },
  hidden: computed('model.status', 'role', 'model.user_id', function(){
    let status = this.get('model.status');
    let role = this.get('role');
    let userId = this.get('session.session.authenticated.id');
    let applicationUserId = this.get('model.user_id');

    if (role === 'USER') {
      let showButtonBy = [false, true, true, true, true, false, true, true, true, true];

      return showButtonBy[status - 1];
    } else if (role === 'MANAGER' && userId === applicationUserId) {
      let showButtonBy = [false, true, true, true, true, false, true, true, true, true];

      return showButtonBy[status - 1];
    } else if (role === 'HELPDESK' && userId === applicationUserId) {
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
  hidden: computed('model.status', 'role', 'model.user_id', function(){
    let status = this.get('model.status');
    let role = this.get('role');
    let userId = this.get('session.session.authenticated.id');
    let applicationUserId = this.get('model.user_id');

    if (role === 'USER') {
      let showButtonBy = [true, false, true, true, true, true, false, true, true, true];

      return showButtonBy[status - 1];
    } else if (role === 'MANAGER' && userId === applicationUserId) {
      let showButtonBy = [true, false, true, true, true, true, false, true, true, true];

      return showButtonBy[status - 1];
    } else if (role === 'HELPDESK' && userId === applicationUserId) {
      let showButtonBy = [true, false, true, true, true, true, false, true, true, true];

      return showButtonBy[status - 1];
    } else if (role === 'SECRETARY') {
      let showButtonBy = [true, true, true, false, false, true, true, true, true, true];

      return showButtonBy[status - 1];
    } else if (role === 'CONTROLLER') {
      let showButtonBy = [true, true, true, true, true, true, true, true, false, false];

      return showButtonBy[status - 1];
    } else if (role === 'PRESIDENT_SECRETARY') {
      let showButtonBy = [true, true, true, true, false, true, true, true, true, false];

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
    message: computed('model.status', function(){
      let status = this.get('model.status');
      if (status === 5) {
        return  'prompt_undo_approve_application_message';
      } else if (status === 10) {
        return 'prompt_undo_approve_compensation_message';
      } else {
        return'prompt_undo_message';
      }
    }),
    title: computed('model.status', function(){
      let status = this.get('model.status');
      if (status === 5) {
        return  'prompt_undo_approve_application_title';
      } else if (status === 10) {
        return 'prompt_undo_approve_compensation_title';
      } else {
        return 'prompt_undo_title';
      }
    }),
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
    let applicationUrl = url + 'application_report/';
    let decisionUrl = url + 'decision_report/';
    let urls = [applicationUrl, decisionUrl];
    messages.setWarning('downloading.started', { closeTimeout: 180000});

    return Promise.all(urls.map((url) => {
      fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': `Token ${token}`,
        }
      }).then((resp) => {
         if (resp.status < 200 || resp.status > 299) {
           throw resp;
         }
         let a = $("<a style='display: none;'/>");
         let url = window.URL.createObjectURL(resp._bodyBlob);
         let namePrefix = resp.url.split('/').slice(-2)[0];
         let name = namePrefix + '_dse[' + dse + ']' + '.pdf';
         a.attr("href", url);
         a.attr("download", name);
         $("body").append(a);
         a[0].click();
         window.URL.revokeObjectURL(url);
         a.remove();
         messages.setSuccess('downloading.finished');
      }).catch((err) => {
         messages.setError('reason.errors');
         throw err;
      });
    }))
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
    } else if (role === 'PRESIDENT_SECRETARY') {
      let showButtonBy = [true, true, true, false, true, true, true, true, false, true];

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
    title: computed('model.status', function(){
      let status = this.get('model.status');
      if (status === 4) {
        return  'prompt_approve_application_title';
      } else if (status === 9) {
        return 'prompt_approve_compensation_title';
      }
    }),
  },
};

const addToTimesheets = {
  label: 'tooltip_addToTimesheets',
  icon: 'today',
  classNames: computed('model.timesheeted', function(){
    let timesheeted = this.get('model.timesheeted');

    if (timesheeted == true) {
      return 'md-fancy';
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


const managerApproval = {
  label: computed('model.manager_movement_approval', function() {
    let managerApproval = this.get('model.manager_movement_approval');

    if (managerApproval == true) {
      return 'tooltip_managerApprovalUndo';
    } else if (managerApproval == false) {
      return 'tooltip_managerApproval';
    }
  }),
  icon: 'check_circle',
  classNames: computed('model.manager_movement_approval', function() {
    let managerApproval = this.get('model.manager_movement_approval');

    if (managerApproval == true) {
      return 'md-success';
    } else if (managerApproval == false) {
      return 'md-neutral';
    }
  }),
  action: function(route, model) {
    let endpoint = 'update_manager_movement_approval';
    let msgSuccess = 'manager.approval.success';
    let msgError = 'manager.approval.error';

    return ajax_call(route, model, endpoint, msgSuccess, msgError);
  },
  hidden: computed('model.status', 'role', 'session', 'model.project.manager_id',  function(){
    let status = this.get('model.status');
    let role = this.get('role');
    let userId = this.get('session.session.authenticated.id');
    let managerId = this.get('model.project.manager_id');

    if (role === 'MANAGER' && userId === managerId) {
      let showButtonBy = [true, false, false, true, true, true, true, true, true, true];

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
      return 'md-danger';
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
    let url = adapter.buildURL('project') + 'stats/';
    messages.setWarning('downloading.file.started', { closeTimeout: 180000});

    return fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': `Token ${token}`,
      }
    }).then((resp) => {
       if (resp.status < 200 || resp.status > 299) {
         throw resp;
       }
       let a = $("<a style='display: none;'/>");
       let url = window.URL.createObjectURL(resp._bodyBlob);
       let name = 'travel_statistics.xlsx';
       a.attr("href", url);
       a.attr("download", name);
       $("body").append(a);
       a[0].click();
       window.URL.revokeObjectURL(url);
       a.remove();
       messages.setSuccess('downloading.file.finished');
    }).catch((err) => {
       messages.setError('reason.errors');
       throw err;
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

const reset = {
  label: 'prompt_reset_title',
  icon: 'looks_3',
  accent: true,
  action: function(route, model) {
    let endpoint = 'reset';
    let msgSuccess = 'reset.application.success';
    let msgError = 'reset.application.error';

    return ajax_call(route, model, endpoint, msgSuccess, msgError);
  },
  hidden: computed('model.status', 'role', function(){
    let status = this.get('model.status');
    let role = this.get('role');

    if (role === 'HELPDESK') {
      let showButtonBy = [true, true, true, false, false, false, false, false, false, false];

      return showButtonBy[status - 1];
    } else {
      return true;
    }
  }),
  confirm: true,
  prompt: {
    ok: 'form.ok.label',
    cancel: 'form.cancel.label',
    message: 'prompt_reset_message',
    title: 'prompt_reset_title',
  },
};

const activate = {
  label: computed('model.is_active', function() {
    let userIsActive = this.get('model.is_active');
    if (userIsActive) {
      return 'prompt_deactivate_title';
    } else {
      return 'prompt_activate_title';
    }
  }),
  icon: computed('model.is_active', function() {
    let userIsActive = this.get('model.is_active');

    if (userIsActive) {
      return 'do_not_disturb_on';
    } else {
      return 'check_circle';
    }
  }),
  classNames: computed('model.is_active', function(){
    let userIsActive = this.get('model.is_active');
    
    if (userIsActive) {
      return 'md-danger';
    } else {
      return 'md-success';
    }
  }),
  action: function(route, model) {
    let userIsActive = model. get('is_active');
    let endpoint = 'toggle_active';
    let msgSuccess = '';
    let msgError = '';

    if (userIsActive) {
      msgSuccess = 'deactivate.user.success';
      msgError = 'deactivate.user.error';
    } else {
      msgSuccess = 'activate.user.success';
      msgError = 'activate.user.error';
    }
    return ajax_call(route, model, endpoint, msgSuccess, msgError);
  },
  hidden: computed('role', function(){
    let role = this.get('role');

    if (role === 'HELPDESK') {
      return false;
    } else {
      return true;
    }
  }),
  confirm: true,
  prompt: {
    ok: 'form.ok.label',
    cancel: 'form.cancel.label',
    message:  computed('model.is_active', function(){
      let userIsActive = this.get('model.is_active');

      if (userIsActive) {
        return 'prompt_deactivate_message';
      } else {
        return 'prompt_activate_message';
      }
    }),
    title:  computed('model.is_active', function(){
      let userIsActive = this.get('model.is_active');

      if (userIsActive) {
        return 'prompt_deactivate_title';
      } else {
        return 'prompt_activate_title';
      }
    }),
  },
};

const markAsDeleted = {
  label: 'prompt_delete_title',
  icon: 'delete_forever',
  classNames:'md-danger',
  action: function(route, model) {
    let endpoint = 'mark_as_deleted';
    let msgSuccess = 'delete.application.success';
    let msgError = 'delete.application.error';

    return ajax_call(route, model, endpoint, msgSuccess, msgError);
  },
  hidden: computed('role', 'model.status', function(){
    let status = this.get('model.status');
    let role = this.get('role');
    let userId = this.get('session.session.authenticated.id');
    let applicationUserId = this.get('model.user_id');

    if (role === 'USER') {
      let showButtonBy = [false, true, true, true, true, true, true, true, true, true];

      return showButtonBy[status - 1];
    } else if (role === 'MANAGER' && userId === applicationUserId) {
      let showButtonBy = [false, true, true, true, true, true, true, true, true, true];

      return showButtonBy[status - 1];
    } else if (role === 'HELPDESK' && userId === applicationUserId) {
      let showButtonBy = [false, true, true, true, true, true, true, true, true, true];

      return showButtonBy[status - 1];
    } else {
      return true;
    }
  }),
  confirm: true,
  prompt: {
    ok: 'form.ok.label',
    cancel: 'form.cancel.label',
    message: 'prompt_delete_message',
    title: 'prompt_delete_title',
  },
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
  managerApproval: managerApproval,
  reset: reset,
  activate: activate,
  markAsDeleted: markAsDeleted,
};

export { applicationActions };
