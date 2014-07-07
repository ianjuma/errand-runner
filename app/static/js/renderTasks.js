function renderTask () {

	console.log(resultData[2]);
	console.log(resultData[1]);

	$('#task-title').html(resultData[0]['task_title']);
	$('#task-desc').html(resultData[0]['task_desc']);
	$('#task-status').html(resultData[0]['task_urgency']);

	$('#task-title2').html(resultData[1]['task_title']);
	$('#task-desc2').html(resultData[1]['task_desc']);
	$('#task-status2').html(resultData[1]['task_urgency']);

	$('#task-title3').html(resultData[2]['task_title']);
	$('#task-desc3').html(resultData[2]['task_desc']);
	$('#task-status3').html(resultData[2]['task_urgency']);

};


function renderTasks(result) {

  _.map(result, function (task) {
    console.log(task);

    $('#allTasks').append('<tr>' +
      '<td>'+ task['task_title'] +'</td>' +
      '<td>'+ task['task_urgency'] +'</td>' +
      '<td>'+ task['task_desc'] +'</td>' +
      '<td><a href=/editTask/' + username + '/' + task['task_id'] + '>' + '#' + task['task_id'] + '</a></td>' +
    '</tr>');
  });
}