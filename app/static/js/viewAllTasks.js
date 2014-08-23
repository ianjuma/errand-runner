function renderTask (result) {

  _.map(result, function (task) {
    console.log(task);

    url = '/task/editTask/' + task['task_id'] + '/';

    $('#taskBody').append(
    '<tr>' +
      '<td>' + task['task_title'] + '</td>' +
      '<td> <a href="' + url + '"> view details </a> </td>' + 
      '<td class="text-right color-success">w47w07q07wr7wq</td>' +
      '<td>' + task['task_urgency'] + '</td>' +
      '<td class="color-success"><div class="progress"><div class="progress-bar progress-bar-danger" style="width: 10%">0%</div></div></td>' +
      '<td class="text-center"><a class="label label-default" href="'+ url + '"><i class="fa fa-pencil"></i></a> <a class="label label-danger" href="' + url + '"><i class="fa fa-times"></i></a></td>' +
    '</tr>'
    );

  });
}

function renderInfo() {
      url = '/task/myTasks/';
      html = '<div class="alert alert-success">' +
          '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' +
          '<i class="fa fa-check sign"></i><strong>You Have no tasks.<a href='+url+'> Create a task</a></strong>' +
      '</div>';
      console.log(url);

      $('#info').append(html);
}

function  getTaskData() {
  
  data = { "username": username };

  taskData = JSON.stringify(data);
  console.log(taskData);
  NProgress.set(0.0);

  $.ajax({
    type: 'POST',
    url: '/api/getTasks/',
    contentType: 'application/json; charset=UTF-8',

    success: function(result) {

      if (result.length == 0) {
        console.log("Empty List");
        renderInfo();
      }

      renderTask(result);
      NProgress.set(1.0);

    },
    fail: function(result) {
      alert('Failed to send Data');
    },
    data: taskData
  });
}