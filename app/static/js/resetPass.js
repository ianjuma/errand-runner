"use strict";


$('#submit-email').click( function sendData () {

    var email = $('#emailData').val();
    var data = { "email": email };
    var userData = JSON.stringify(data);
    console.log(userData);

    $.ajax({
      type: "POST",
      url: '/reset/',
      data: jsonData,
      contentType: "application/json; charset=UTF-8",
      dataType: "json",

      success: function(result) {
        console.log(result);
        window.location.href = "/";
      },
      fail: function(result) {
        alert('Failed to send Data');
      },

      data: userData
    });
  }
);