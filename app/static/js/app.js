$('#loginData').click( function() {

        passd = $('#pw').val();
        passd2 = $('#pwtwo').val();

        email = $('#email').val();
        username = $('#getmobileNo').val(); // verification

        if ($('#getmobileNo').val() == "") {
          alert('You need a valid username');
          return 0;
        }

        if ($('#getmobileNo').val().length < 3) {
          alert('Your username is too short');
          return 0;
        }


        if ($('#pw').val() == "") {
          alert('You need a valid password');
          return 0;
        }

        if (passd == "" || passd.length < 5) {
          alert("Your password is too short or empty");
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
          contentType: 'application/json',
          success: function(result) {
            console.log(result);
            window.location.replace("/profile/"+username);
          },
          fail: function(result) {
            alert('Failed to send Data');
          },

          data: userData
        });
});


$('#signInData').click( function() {

  username = $('#mobileNo').val();
  passwd = $('#getPass').val();


  data = { "username": username, "password": passwd };
  userData = JSON.stringify(data);
  console.log(userData);

  $.ajax({
    type: 'POST',
    url: '/api/signIn/',
    contentType: 'application/json',

    success: function(result) {
      console.log(result);
      window.location.replace("/tasks/"+username);
    },
    fail: function(result) {
      alert('Failed to send Data');
    },

    data: userData
  });
});