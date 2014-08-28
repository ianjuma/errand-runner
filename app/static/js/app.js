function validateEmail(email) { 
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

$('#loginData').click( function(evnt) {
        evnt.preventDefault();

        passd = $('#pw').val();
        passd2 = $('#pwtwo').val();

        email = $('#email').val();
        username = $('#getmobileNo').val(); // verification

        if (!validateEmail(email)) {
          alert('Please enter a valid email');
        }

        if ($('#getmobileNo').val() == "") {
          alert('You need a valid username');
          return 0;
        }

        if ($('#getmobileNo').val().length < 3) {
          alert('Your username is too short, at least 5 characters');
          return 0;
        }

        if ($('#pw').val() == "") {
          alert('Password field is empty');
          return 0;
        }

        if (passd == "" || passd.length < 5) {
          alert("Your password is too short or empty, at least 6 characters");
          return 0;
        }

        if (passd != passd2) {
          alert("Passwords don't match");
          return 0;
        }

        data = { "email": email, "password": passd, "username": username };
        userData = JSON.stringify(data);
        console.log(userData);

        $.ajax({
          type: 'POST',
          url: '/api/signUp/',
          contentType: 'application/json; charset=UTF-8',
          datatype: "json",
          cache: false,
          timeout: 60000,
          async: true,
          success: function(result, textStatus, jqXHR) {
            console.log(result);
            window.location.href = "/profile/";
          },
          fail: function(result, textStatus, jqXHR) {
            alert('Failed to send Data');
          },

          data: userData
        });
});


$('#signInData').click( function(evnt) {
  evnt.preventDefault();
  
  username = $('#mobileNo').val();
  passwd = $('#getPass').val();

  if ( username == "" ) {
    alert('You need a valid username');
    return 0;
  }

  if ( passwd == "" ) {
    alert('Password cannot be empty');
    return 0;
  }


  data = { "username": username, "password": passwd };
  userData = JSON.stringify(data);
  console.log(userData);
  

  $.ajax({
    data: userData,
    type: 'POST',
    dataType: 'json',
    contentType: 'application/json; charset=UTF-8',
    url: '/api/signIn/',

    success: function(result) {
      console.log(result);
      window.location.href = "/task/myTasks/";
    },
    error: function(result) {
      console.log(result);
      alert('The username or password provided is incorrect');
    }
  });
});