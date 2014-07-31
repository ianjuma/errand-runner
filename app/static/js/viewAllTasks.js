function renderTask (result) {

  _.map(result, function (task) {
    console.log(task);

    url = '/editTask/' + username + '/' + task['task_id'] + '/';

    $('#taskBody').append(
    '<tr>' +
      '<td><input type="checkbox" />' + task['task_title'] + '</td>' +
      '<td> view details </td>' +
      '<td class="text-right color-success">w47w07q07wr7wq</td>' +
      '<td>' + task['task_urgency'] + '</td>' +
      '<td class="color-success"><div class="progress"><div class="progress-bar progress-bar-success" style="width: 40%">40%</div></div></td>' +
      '<td class="text-center"><a class="label label-default" href="'+ url + '"><i class="fa fa-pencil"></i></a> <a class="label label-danger" href="' + url + '"><i class="fa fa-times"></i></a></td>' +
    '</tr>'
    );

  });
}


function  getTaskData() {
  
  data = { "username": username };

  taskData = JSON.stringify(data);
  console.log(taskData);
  NProgress.set(0.0);

  $.ajax({
    type: 'POST',
    url: '/api/getTasks/',
    contentType: 'application/json',

    success: function(result) {
      // console.log(result);
      renderTask(result);
      NProgress.set(1.0);

    },
    fail: function(result) {
      alert('Failed to send Data');
    },
    data: taskData
  });
}