$('#update-task').click( function(evnt) {
  evnt.preventDefault();

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

  if ($('#reservation').val() == "") {
    alert('Your task needs due date');
    return 0;
  }

  if ($('#locationData').val() == "") {
    alert('Your task needs location information');
    return 0;
  }

  if (typeof($('#locationData').val()) != "string") {
    alert('please enter location of task');
    return 0;
  }

  if ($('#contactPersons').val() == "") {
    alert('Your task needs contact information');
    return 0;
  }

  task_title = $('#taskTitle-data').val();
  task_desc = $('#task-desc').val();
  task_urgency = $('#urgent-data').val();
  reservation = $('#reservation').val();
  task_category = $('#category-data').val();
  contactPersons = $('#contactPersons').val();
  locationData = $('#locationData').val();
  contactPersons = $('#contactPersons').val();

  console.log("in update");

  data = { "task_id": task_id, "username": username, "title": task_title, "description": task_desc,
                "due_date": reservation, "contactPersons": contactPersons, "locationData": locationData, 
                "task_urgency": task_urgency };

  userData = JSON.stringify(data);

  NProgress.set(0.0);

  $.ajax({
    type: 'POST',
    url: '/api/editTask/'+ task_id + '/',
    contentType: 'application/json; charset=UTF-8',

    success: function(result) {
      console.log(result);

      NProgress.set(1.0);

      $.gritter.add({
        title: 'Task Updated',
        text: 'Task Successfully Updated',
        class_name: 'success'
      });

    },
    fail: function(result) {
      alert('Failed to send Data');
    },

    data: userData
  });

  console.log(userData);
});


$('#delete-task').click( function(evnt) {
  evnt.preventDefault();

  NProgress.set(0.0);
  data = { "task_id": task_id, "username": username };

  userData = JSON.stringify(data);

  $.ajax({
    type: 'POST',
    url: '/api/deleteTask/',
    contentType: 'application/json; charset=UTF-8',

    success: function(result) {
      console.log(result);

      NProgress.set(1.0);

      $.gritter.add({
        title: 'Task Updated',
        text: 'Task Successfully Deleted',
        class_name: 'success'
      });

    },
    fail: function(result) {
      alert('Failed to send Data');
    },

    data: userData
  });

  console.log(userData);

});


$('#add-task').click( function(evnt) {
  evnt.preventDefault();
  
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
    contentType: 'application/json; charset=UTF-8',

    success: function(result) {
      console.log(result);
      NProgress.set(1.0);
      var n = noty({text: 'Task Updated!', layout: "topRight", type: "information"});

    },
    fail: function(result) {
      alert('Failed to send Data');
      var n = noty({text: 'Task Update Failed!', layout: "topRight", type: "information"});
    },

    data: userData
  });

  console.log(userData);
});