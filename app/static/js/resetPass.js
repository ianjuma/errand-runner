"use strict";

$('#submit-email').click( function sendData () {

    var email = $('#emailData').val();
    var data = { "email": email };
    var userData = JSON.stringify(data);
    console.log(userData);

    $.ajax({
      type: "POST",
      url: '/reset/',
      contentType: "application/json; charset=UTF-8",
      dataType: "json",

      success: function(result) {
        console.log(result);

        $.gritter.add({
          title: 'Password Reset',
          text: 'New Password has been sent to your email',
          class_name: 'success'
        });

        window.location.href = "/";
      },
      fail: function(result) {
        alert('Failed to send Data');
      },

      data: userData
    });
  }
);