$('#completeAll').click( function(evnt) {
  evnt.preventDefault();

  if ($('#taskCat').val() == "") {
    alert('Your task needs a category');
    return 0;
  }

  if (typeof($('#taskCat').val()) != "string") {
    alert('Your task category should be in text form');
    return 0;
  }

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


  if ($('#locationData').val() == "") {
    alert('Your Task needs a due date');
    return 0;
  }

  if (typeof($('#contactPersons').val()) != "string") {
    alert('Your date needs to be in text form');
    return 0;
  }

  //validate();
  task_title = $('#taskTitle-data').val();
  task_desc = $('#task-desc').val();
  task_urgency = $('#urgent-data').val();
  date_data = $('#reservation').val();
  my_location = $('#locationData').val();
  task_category = $('#taskCat').val();
  contact_p = $('#contactPersons').val();


  data = { "username": username, "title": task_title, "description": task_desc, "urgency": task_urgency,
              "due_date": date_data, "category": task_category, "contactPersons": contact_p, "locationData": my_location };

  userData = JSON.stringify(data);
  console.log(data);

  NProgress.set(0.5);
  $.ajax({
    type: 'POST',
    url: '/api/addTask/',
    contentType: 'application/json; charset=UTF-8',

    success: function(result) {
      console.log(result);
      
      NProgress.set(1.0);
      console.log("Sending Data ... ");

      $.gritter.add({
        title: 'Success',
        text: 'Task Successfully Created',
        class_name: 'success'
      });

      window.location.href = '/process_payments/';
    },
    always: function(result) {
      console.log(result);
    },

    fail: function(result) {
      // gritter fail
    },

    data: userData
  });

  console.log(userData);
});



function validate() {
  // validate all inputs
  task_title = $('#taskTitle-data').val();
  task_desc = $('#task-desc').val();
  task_urgency = $('#urgent-data').val();
  date_data = $('#reservation').val();
  location = $('#locationData').val();
  task_category = $('#taskCat').val();
  contact_p = $('#contactPersons').val();


  if ($('#taskCat').val() == "") {
    alert('Your task needs a category');
    return 0;
  }

  if (typeof($('#taskCat').val()) != "string") {
    alert('Your task category should be in text form');
    return 0;
  }

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


  if ($('#locationData').val() == "") {
    alert('Your Task needs a due date');
    return 0;
  }

  if (typeof($('#contactPersons').val()) != "string") {
    alert('Your date needs to be in text form');
    return 0;
  }
}


$('#updateUserInfo').click( function(evnt) {
  evnt.preventDefault();

  if ($('#firstname').val() == "") {
    alert('Please enter your first name');
    return 0;
  }

  if (typeof($('#firstname').val()) != "string") {
    alert('please enter a valid name');
    return 0;
  }

  if ($('#lastname').val() == "") {
    alert('Enter your last name');
    return 0;
  }

  if (typeof($('#lastname').val()) != "string") {
    alert('Please enter a valid last name');
    return 0;
  }


  if ($('#mobileNo').val() == "") {
    alert('Please enter your mobile number');
    return 0;
  }

  if ($('#country').val() == "") {
    alert('Please enter your country');
    return 0;
  }

  first_name = $('#firstname').val();
  last_name = $('#lastname').val();
  email = $('#email').val();
  mobileNo = $('#mobileNo').val();
  password = $('#password').val();
  state = $('#country').val();

  data = { "username": username, "firstname": first_name, "lastname": last_name, "state": state, 
              "email": email, "password": password, "mobileNo": mobileNo, "dob": "", "last_name": last_name };

  userData = JSON.stringify(data);
  NProgress.set(0.0);

  console.log('Data sent');
  $.ajax({
    type: 'POST',
    url: '/profile/',
    contentType: 'application/json; charset=UTF-8',

    success: function(result) {
      console.log(result);
      NProgress.set(1.0);
      
      $.gritter.add({
        title: 'User Info Updated',
        text: 'User Information Updated',
        class_name: 'success'
      });
    },
    fail: function(result) {
      $.gritter.add({
        title: 'Update Failed',
        text: 'Failed',
        class_name: 'failure'
      });
    },

    data: userData
  });

  console.log(userData);
});


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
      // console.log(result);
      renderSample(result);
      NProgress.set(1.0);

    },
    fail: function(result) {
      alert('Failed to send Data');
    },
    data: taskData
  });
}

function renderSample (package) {

    _.map(package, function (task) {
      console.log(task);

    var task_summary;

    if (task['task_title'] === "") {
      task_summary = '<li href="#" class="list-group-item"><span class="date"><i class="fa fa-clock-o"></i>' + 
     '20 Dec </span> Task Title undefined</li>'
    } else {
      task_summary = '<li href="#" class="list-group-item"><span class="date"><i class="fa fa-clock-o"></i>' + 
      '20 Dec </span>' + task['task_title'] + '</li>'
    }

    $('#addTo').append(task_summary);
    });
}