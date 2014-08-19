function renderTask (result) {

  _.map(result, function (task) {
    console.log(task);

    $('#taskBody').append('<tr>' +
      '<td>'+ task['task_title'] +'</td>' +
      '<td>'+ task['task_urgency'] +'</td>' +
      '<td>'+ task['task_desc'] +'</td>' +
      '<td><a href="#">#' + task['task_id'] + '</a></td>' +
    '</tr>');
  });
}


function  getTaskData() {
  
  data = { "username": "username", "task_urgency": "started" };

  taskData = JSON.stringify(data);
  console.log(taskData);
  NProgress.set(0.0);

  $.ajax({
    type: 'POST',
    url: '/adminTasks/',
    contentType: 'application/json; charset=UTF-8',

    success: function(result) {
      // console.log(result);
      size = _.size(result);
      console.log(size);
      $("badge-task-no").val(size);

      renderTask(result);
      NProgress.set(1.0);

    },
    fail: function(result) {
      alert('Failed to send Data');
    },
    data: taskData
  });
}