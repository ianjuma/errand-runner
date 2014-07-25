$('#clear-all').click( function() {
  $('#taskTitle-data').val("");
  $('#task-desc').val("");
  $('#urgent-data').val("");

  console.log("All cleaned");
});


$('#completeAll').click( function() {
  task_title = $('#taskTitle-data').val();
  task_desc = $('#task-desc').val();
  task_urgency = $('#urgent-data').val();
  date_data = $('#reportrange').val();
  location = $('#locationData').val();
  task_category = $('#category-data').val();
  contact_p = $('#contactPersons').val();


  data = { "username": username, "title": task_title, "description": task_desc, "urgency": task_urgency,
                "due_date": date_data, "category": task_category, "contact_p": contact_p };

  userData = JSON.stringify(data);

  NProgress.set(0.0);
  $.ajax({
    type: 'POST',
    url: '/api/addTask/',
    contentType: 'application/json',

    success: function(result) {
      console.log(result);
      
      $.gritter.add({
          title: 'Task Saved!',
          text: 'Your Task has been saved',
          class_name: 'success'
        });
      NProgress.set(1.0);

      window.location.href = '/';

    },
    fail: function(result) {
      // gritter fail
      $.gritter.add({
          title: 'Oops',
          text: 'Your Task Could not be saved',
          class_name: 'success'
        });
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


  data = { "username": username, "title": task_title, "description": task_desc, "urgency": task_urgency,
                "due_date": date_data, "category": task_category };

  userData = JSON.stringify(data);

  NProgress.set(0.0);

  $.ajax({
    type: 'POST',
    url: '/api/addTask/',
    contentType: 'application/json',

    success: function(result) {
      console.log(result);
      var n = noty({text: 'Task saved!', layout: "topRight", type: "information"});

      NProgress.set(1.0);

    },
    fail: function(result) {
      var n = noty({text: 'Oops something went wrong, Task could not be saved!', layout: "topRight", type: "information"});
    },

    data: userData
  });

  console.log(userData);
});