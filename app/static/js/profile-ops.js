$('#clear-all').click( function() {
  $('#name-data').val("");
  $('#state-data').val("");
  $('#c_password-data').val("");
  $('#password-data').val("");
  $('#password2-data').val("");
  $('#sms-data').val("");
  $('#email-data').val("");
  $('#mobile-data').val("");

  console.log("All cleaned");
});

$('#save-data').click( function() {
  task_title = $('#taskTitle-data').val();
  task_desc = $('#task-desc').val();
  task_urgency = $('#urgent-data').val();
  date_data = $('#date-data').val();
  task_category = $('#category-data').val();
  mobile_data = $('#mobile-data').val();


  data = { "username": username, "mobileNo": mobile_data ,"title": task_title, "description": task_desc, "urgency": task_urgency,
                "due_date": date_data, "category": task_category };

  userData = JSON.stringify(data);
  NProgress.set(0.0);

  $.ajax({
    type: 'POST',
    url: '/api/addTask/',
    contentType: 'application/json',

    success: function(result) {
      console.log(result);
      NProgress.set(1.0);
    },
    fail: function(result) {
      alert('Failed to send Data');
    },

    data: userData
  });

  console.log(userData);
});


$('#delete-data').click( function() {

  c_password = $('#c_password-data').val();
  username = $(username).val();


  data = { "username": username, "password": c_password };

  userData = JSON.stringify(data);

  NProgress.set(0.0);
  $.ajax({
    type: 'POST',
    url: '/api/removeUser/',
    contentType: 'application/json',

    success: function(result) {
      NProgress.set(1.0);
      console.log(result);
      var n = noty({text: 'Account Deleted!', layout: "topRight", type: "information"});
      window.location.href = '/';
    },
    fail: function(result) {
      alert('Failed to send Data');
    },

    data: userData
  });

  console.log(userData);
});


$('#save-user').click( function() {

  name = $('#name-data').val();
  state = $('#state-data').val();
  email = $('#email-data').val();
  smsdata = $('#sms-data').val();
  dob = $('#date-data').val();
  password = $('#c_password-data').val();
  mobileNo = $('#mobile-data').val();

  if ($('#name-data').val() == "") {
    alert('Please enter your name');
    return 0;
  }

  if ($('#state-data').val() == "") {
    alert('Please enter your country');
    return 0;
  }

  if ($('#mobile-data').val() == "") {
    alert('Please enter a valid number');
    return 0;
  }

  if ($('#sms-data').val() == "") {
    alert('Please enter your sms code');
    return 0;
  }

  if ($('#date-data').val() == "") {
    alert('Please enter your date of birth');
    return 0;
  }

  data = { "username": name, "state": state, "password": password,
                "dob": dob, "email": email, "smsdata": smsdata, "mobileNo": mobileNo };

  userData = JSON.stringify(data);

  NProgress.set(0.0);
  $.ajax({
    type: 'POST',
    url: '/profile/'+username+'/',
    contentType: 'application/json',

    success: function(result) {
      NProgress.set(1.0);
      console.log(result);
      var n = noty({text: 'Task Updated!', layout: "topRight", type: "information"});
    },
    fail: function(result) {
      alert('Failed to send Data');
    },

    data: userData
  });

  console.log(userData);
});
