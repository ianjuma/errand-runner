$('#clear-all').click( function() {
  $('#taskTitle-data').val("");
  $('#task-desc').val("");
  $('#urgent-data').val("");

  console.log("All cleaned");
});


$('#save-data').click( function() {
  task_title = $('#taskTitle-data').val();
  task_desc = $('#task-desc').val();
  task_urgency = $('#urgent-data').val();
  date_data = $('#date-data').val();
  task_category = $('#category-data').val();


  data = { "task_id": task_id, "username": username, "title": task_title, "description": task_desc, "urgency": task_urgency,
                "due_date": date_data, "category": task_category };

  userData = JSON.stringify(data);

  NProgress.set(0.0);

  $.ajax({
    type: 'POST',
    url: '/api/editTask/'+ task_id + '/',
    contentType: 'application/json',

    success: function(result) {
      console.log(result);
      console.log(result.response);
      $.notify("Task Updated!", "success");
      $("#add-task").notify(
        "Task Updated!",
        { position:"bottom" }
      );
      NProgress.set(1.0);

    },
    fail: function(result) {
      alert('Failed to send Data');
    },

    data: userData
  });

  console.log(userData);
});


$('#add-task').click( function() {
  task_title = $('#taskTitle-data').val();
  task_desc = $('#task-desc').val();
  task_urgency = $('#urgent-data').val();
  date_data = $('#date-data').val();
  task_category = $('#category-data').val();

  if ($('#taskTitle-data').val() == "") {
    alert('Your task needs a title');
    return 0;
  }

  if (typeof($('#taskTitle-data').val()) != "string") {
    alert('Your task needs in text form');
    return 0;
  }


  if ($('#task-desc').val() == "") {
    alert('Your Task needs a description');
    return 0;
  }

  if (typeof($('#task-desc').val()) != "string") {
    alert('Your description needs to be in text form');
    return 0;
  }


  if ($('#date-data').val() == "") {
    alert('Your Task needs a date');
    return 0;
  }

  if (typeof($('#date-data').val()) != "string") {
    alert('Your date needs to be in text form');
    return 0;
  }


  data = { "task_id": task_id, "username": username, "title": task_title, "description": task_desc, "urgency": task_urgency,
                "due_date": date_data, "category": task_category };

  userData = JSON.stringify(data);

  NProgress.set(0.0);
  $.ajax({
    type: 'PUT',
    url: '/api/editTask/'+task_id + '/',
    contentType: 'application/json',

    success: function(result) {
      console.log(result);
      $.notify("Task Updated!", "success");

      $("#add-task").notify(
        "Task Updated!", "success",
        { position:"bottom" }
      );
      NProgress.set(1.0);

    },
    fail: function(result) {
      alert('Failed to send Data');
    },

    data: userData
  });

  console.log(userData);
});